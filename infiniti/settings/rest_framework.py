REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'otp_verification': '10/hour',
    }
}