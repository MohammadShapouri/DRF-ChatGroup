from django.test import TestCase
from .utils.base_OTP_config_manager import BaseOTPConfigManager
# Create your tests here.


class BaseOTPConfigManagerTestClass(TestCase):
    maxDiff = None

    def test_config_creation1(self):
        config = None
        base_OTP_config_manager_object = BaseOTPConfigManager()
        base_OTP_config_manager_object._create_config(config)
        expected_config_profiles = {
            'account_verification':{
                'OTP_type': 'timer_counter_based',
                'OTP_usage': 'Account Verification',
                'max_possible_try': 5,
                'expire_after': 60,
                'OTP_length': base_OTP_config_manager_object.default_OTP_length
            },
            'new_phone_number_verification': {
                'OTP_type': 'counter_based',
                'OTP_usage': 'New Phone Number Verification',
                'max_possible_try': 5,
                'OTP_length': base_OTP_config_manager_object.default_OTP_length
            },
            'reset_password': {
                'OTP_type': 'timer_based',
                'OTP_usage': 'Forgotten Password',
                'expire_after': 60,
                'OTP_length': base_OTP_config_manager_object.default_OTP_length
            }
        }
        self.assertEqual(base_OTP_config_manager_object.default_OTP_length, 8)
        self.assertEqual(base_OTP_config_manager_object.default_max_possible_try, 5)
        self.assertEqual(base_OTP_config_manager_object.default_expire_after, 60)
        self.assertDictEqual(base_OTP_config_manager_object.config_profiles, expected_config_profiles)
        self.assertListEqual(list(base_OTP_config_manager_object.config_profiles.keys()), list(expected_config_profiles.keys()))



    def test_config_creation2(self):
        config = {
            'default_OTP_length': 19, 
            'default_max_possible_try': 81,
            'default_expire_after': 37,
        }
        base_otp_config_manager_object = BaseOTPConfigManager()
        base_otp_config_manager_object._create_config(config)
        expected_config_profiles = {
            'account_verification':{
                'OTP_type': 'timer_counter_based',
                'OTP_usage': 'Account Verification',
                'max_possible_try': base_otp_config_manager_object.default_max_possible_try,
                'expire_after': base_otp_config_manager_object.default_expire_after,
                'OTP_length': base_otp_config_manager_object.default_OTP_length
            },
            'new_phone_number_verification': {
                'OTP_type': 'counter_based',
                'OTP_usage': 'New Phone Number Verification',
                'max_possible_try': base_otp_config_manager_object.default_max_possible_try,
                'OTP_length': base_otp_config_manager_object.default_OTP_length
            },
            'reset_password': {
                'OTP_type': 'timer_based',
                'OTP_usage': 'Forgotten Password',
                'expire_after': base_otp_config_manager_object.default_expire_after,
                'OTP_length': base_otp_config_manager_object.default_OTP_length
            }
        }
        self.assertEqual(base_otp_config_manager_object.default_OTP_length, 19)
        self.assertEqual(base_otp_config_manager_object.default_max_possible_try, 81)
        self.assertEqual(base_otp_config_manager_object.default_expire_after, 37)
        self.assertDictEqual(base_otp_config_manager_object.config_profiles, expected_config_profiles)
        self.assertListEqual(list(base_otp_config_manager_object.config_profiles.keys()), list(expected_config_profiles.keys()))



    def test_config_creation3(self):
        config = {
            'config_profiles':{
                'test_account_verification':{
                    'OTP_type': 'timer_counter_based',
                    'OTP_usage': 'Account Verification',
                },
                'test_new_phone_number_verification': {
                    'OTP_type': 'counter_based',
                    'OTP_usage': 'New Phone Number Verification',
                    'max_possible_try': 39,
                },
                'test_reset_password': {
                    'OTP_type': 'timer_based',
                    'OTP_usage': 'Forgotten Password',
                    'OTP_length': 13
                }
            }
        }
        base_otp_config_manager_object = BaseOTPConfigManager()
        base_otp_config_manager_object._create_config(config)
        expected_config_profiles = {
            'test_account_verification':{
                'OTP_type': 'timer_counter_based',
                'OTP_usage': 'Account Verification',
                'max_possible_try': base_otp_config_manager_object.default_max_possible_try,
                'expire_after': base_otp_config_manager_object.default_expire_after,
                'OTP_length': base_otp_config_manager_object.default_OTP_length
            },
            'test_new_phone_number_verification': {
                'OTP_type': 'counter_based',
                'OTP_usage': 'New Phone Number Verification',
                'max_possible_try': 39,
                'OTP_length': base_otp_config_manager_object.default_OTP_length
            },
            'test_reset_password': {
                'OTP_type': 'timer_based',
                'OTP_usage': 'Forgotten Password',
                'expire_after': base_otp_config_manager_object.default_expire_after,
                'OTP_length': 13
            }
        }
        self.assertEqual(base_otp_config_manager_object.default_OTP_length, 8)
        self.assertEqual(base_otp_config_manager_object.default_max_possible_try, 5)
        self.assertEqual(base_otp_config_manager_object.default_expire_after, 60)
        self.assertDictEqual(base_otp_config_manager_object.config_profiles, expected_config_profiles)
        self.assertListEqual(list(base_otp_config_manager_object.config_profiles.keys()), list(expected_config_profiles.keys()))



    def test_config_creation4(self):
        config = {
            'default_OTP_length': 11, 
            'default_max_possible_try': 22,
            'default_expire_after': 33,
            'config_profiles':{
                'test_account_verification':{
                    'OTP_type': 'timer_counter_based',
                    'OTP_usage': 'Account Verification',
                },
                'test_reset_password': {
                    'OTP_type': 'timer_based',
                    'OTP_usage': 'Forgotten Password',
                    'OTP_length': 13
                }
            }
        }
        base_otp_config_manager_object = BaseOTPConfigManager()
        base_otp_config_manager_object._create_config(config)
        expected_config_profiles = {
            'test_account_verification':{
                'OTP_type': 'timer_counter_based',
                'OTP_usage': 'Account Verification',
                'max_possible_try': base_otp_config_manager_object.default_max_possible_try,
                'expire_after': base_otp_config_manager_object.default_expire_after,
                'OTP_length': base_otp_config_manager_object.default_OTP_length
            },
            'test_reset_password': {
                'OTP_type': 'timer_based',
                'OTP_usage': 'Forgotten Password',
                'expire_after': base_otp_config_manager_object.default_expire_after,
                'OTP_length': 13
            }
        }
        self.assertEqual(base_otp_config_manager_object.default_OTP_length, 11)
        self.assertEqual(base_otp_config_manager_object.default_max_possible_try, 22)
        self.assertEqual(base_otp_config_manager_object.default_expire_after, 33)
        self.assertDictEqual(base_otp_config_manager_object.config_profiles, expected_config_profiles)
        self.assertListEqual(list(base_otp_config_manager_object.config_profiles.keys()), list(expected_config_profiles.keys()))
