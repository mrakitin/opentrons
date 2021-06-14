import React from 'react'
import { FormikConfig } from 'formik'
import { render, screen } from '@testing-library/react'
import '@testing-library/jest-dom'
import { getDefaultFormState, LabwareFields } from '../../../fields'
import { Preview } from '../../sections/Preview'
import { wrapInFormik } from '../../utils/wrapInFormik'
import { FORM_LEVEL_ERRORS } from '../../../formLevelValidation'

// NOTE(IL, 2021-05-18): eventual dependency on definitions.tsx which uses require.context
// would break this test (though it's not directly used)
jest.mock('../../../../definitions')

let formikConfig: FormikConfig<LabwareFields>

describe('Preview', () => {
  beforeEach(() => {
    formikConfig = {
      initialValues: getDefaultFormState(),
      onSubmit: jest.fn(),
    }
  })

  afterEach(() => {
    jest.restoreAllMocks()
  })

  it('should render the preview section', () => {
    render(wrapInFormik(<Preview />, formikConfig))
    expect(screen.getByRole('heading')).toHaveTextContent(/check your work/i)
    screen.getByText(
      'Check that the size, spacing, and shape of your wells looks correct.'
    )
    screen.getByText('Add missing info to see labware preview')
  })

  it('should render form-level alerts when form-level errors are present', () => {
    const FAKE_ERROR = 'ahh'
    // @ts-expect-error: fake form-level error
    formikConfig.initialErrors = { [FORM_LEVEL_ERRORS]: { FAKE_ERROR } }
    render(wrapInFormik(<Preview />, formikConfig))

    // TODO(IL, 2021-05-26): AlertItem should have role="alert", then we can `getByRole('alert', {name: FAKE_ERROR})`
    screen.getByText(FAKE_ERROR)
  })
})