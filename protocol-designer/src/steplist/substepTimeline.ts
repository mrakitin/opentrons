import last from 'lodash/last'
import pick from 'lodash/pick'
import {
  getWellsForTips,
  getNextRobotStateAndWarningsSingleCommand,
} from '@opentrons/step-generation'
import { Command } from '@opentrons/shared-data/protocol/flowTypes/schemaV6'
import { Channels } from '@opentrons/components'
import {
  CommandCreatorError,
  CommandsAndWarnings,
  CurriedCommandCreator,
  InvariantContext,
  RobotState,
} from '@opentrons/step-generation'
import { SubstepTimelineFrame, SourceDestData, TipLocation } from './types'

/** Return last picked up tip in the specified commands, if any */
export function _getNewActiveTips(
  commands: Command[]
): TipLocation | null | undefined {
  const lastNewTipCommand: Command | null | undefined = last(
    commands.filter(c => c.command === 'pickUpTip')
  )
  const newTipParams =
    (lastNewTipCommand != null &&
      lastNewTipCommand.command === 'pickUpTip' &&
      lastNewTipCommand.params) ||
    null
  return newTipParams
}

const _createNextTimelineFrame = ({
  command,
  index,
  nextFrame,
  volume,
  wellInfo,
}: {
  command: Command
  index: number
  nextFrame: CommandsAndWarnings
  volume: number
  wellInfo: SourceDestData
}) => {
  // TODO(IL, 2020-02-24): is there a cleaner way to create newTimelineFrame
  // and keep Flow happy about computed properties?
  const _newTimelineFrameKeys = {
    volume,
    activeTips: _getNewActiveTips(nextFrame.commands.slice(0, index)),
  }
  const newTimelineFrame =
    command.command === 'aspirate'
      ? { ..._newTimelineFrameKeys, source: wellInfo }
      : { ..._newTimelineFrameKeys, dest: wellInfo }
  return newTimelineFrame
}

type SubstepTimelineAcc = {
  timeline: SubstepTimelineFrame[]
  errors: CommandCreatorError[] | null | undefined
  prevRobotState: RobotState
}
export const substepTimelineSingleChannel = (
  commandCreator: CurriedCommandCreator,
  invariantContext: InvariantContext,
  initialRobotState: RobotState
): SubstepTimelineFrame[] => {
  const nextFrame = commandCreator(invariantContext, initialRobotState)
  if (nextFrame.errors) return []
  const timeline = nextFrame.commands.reduce<SubstepTimelineAcc>(
    (acc, command: Command, index) => {
      const nextRobotState = getNextRobotStateAndWarningsSingleCommand(
        command,
        invariantContext,
        acc.prevRobotState
      ).robotState

      if (command.command === 'aspirate' || command.command === 'dispense') {
        const { well, volume, labware } = command.params
        const wellInfo = {
          labware,
          wells: [well],
          preIngreds: acc.prevRobotState.liquidState.labware[labware][well],
          postIngreds: nextRobotState.liquidState.labware[labware][well],
        }
        return {
          ...acc,
          timeline: [
            ...acc.timeline,
            _createNextTimelineFrame({
              volume,
              index,
              nextFrame,
              command,
              // $FlowFixMe(sa, 2021-05-10): ignore until TS conversion
              wellInfo,
            }),
          ],
          prevRobotState: nextRobotState,
        }
      } else {
        return { ...acc, prevRobotState: nextRobotState }
      }
    },
    {
      timeline: [],
      errors: null,
      prevRobotState: initialRobotState,
    }
  )
  return timeline.timeline
}
// timeline for multi-channel substep context
export const substepTimelineMultiChannel = (
  commandCreator: CurriedCommandCreator,
  invariantContext: InvariantContext,
  initialRobotState: RobotState,
  channels: Channels
): SubstepTimelineFrame[] => {
  const nextFrame = commandCreator(invariantContext, initialRobotState)
  if (nextFrame.errors) return []
  const timeline = nextFrame.commands.reduce<SubstepTimelineAcc>(
    (acc, command: Command, index) => {
      const nextRobotState = getNextRobotStateAndWarningsSingleCommand(
        command,
        invariantContext,
        acc.prevRobotState
      ).robotState

      if (command.command === 'aspirate' || command.command === 'dispense') {
        const { well, volume, labware } = command.params
        const labwareDef = invariantContext.labwareEntities
          ? invariantContext.labwareEntities[labware].def
          : null
        const wellsForTips =
          channels &&
          labwareDef &&
          getWellsForTips(channels, labwareDef, well).wellsForTips
        const wellInfo = {
          labware,
          wells: wellsForTips || [],
          preIngreds: wellsForTips
            ? pick(
                acc.prevRobotState.liquidState.labware[labware],
                wellsForTips
              )
            : {},
          postIngreds: wellsForTips
            ? pick(nextRobotState.liquidState.labware[labware], wellsForTips)
            : {},
        }
        return {
          ...acc,
          timeline: [
            ...acc.timeline,
            _createNextTimelineFrame({
              volume,
              index,
              nextFrame,
              command,
              wellInfo,
            }),
          ],
          prevRobotState: nextRobotState,
        }
      } else {
        return { ...acc, prevRobotState: nextRobotState }
      }
    },
    {
      timeline: [],
      errors: null,
      prevRobotState: initialRobotState,
    }
  )
  return timeline.timeline
}
export const substepTimeline = (
  commandCreator: CurriedCommandCreator,
  invariantContext: InvariantContext,
  initialRobotState: RobotState,
  channels: Channels
): SubstepTimelineFrame[] => {
  if (channels === 1) {
    return substepTimelineSingleChannel(
      commandCreator,
      invariantContext,
      initialRobotState
    )
  } else {
    return substepTimelineMultiChannel(
      commandCreator,
      invariantContext,
      initialRobotState,
      channels
    )
  }
}