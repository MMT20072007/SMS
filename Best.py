import random
import time

class CircuitBreaker:
    def __init__(self, services, max_errors, cooldown_time, max_retries=3):
        self.services = services
        self.max_errors = max_errors
        self.cooldown_time = cooldown_time
        self.errors = {service: 0 for service in services}
        self.last_error_time = {service: None for service in services}
        self.current_service = random.choice(services)
        self.max_retries = max_retries

    def send_sms(self, message):
        if all(
            error >= self.max_errors
            and last_error_time is not None
            and time.time() - last_error_time < self.cooldown_time
            for service, error in self.errors.items()
            for last_error_time in [self.last_error_time[service]]
        ):
            print("Circuit Breaker is active. Retry after cooldown period.")
            return

        assert isinstance(message, str)
        assert len(message) > 0

        for service in self.services:
            try:
                service.send_sms(message)
                print("SMS sent successfully.")
                self.errors[service] = 0
                return
            except Exception as e:
                print(f"Error sending SMS: {str(e)}")
                self.errors[service] += 1
                self.last_error_time[service] = time.time()

        print("No available services.")

    def retry(self, message):
        for i in range(self.max_retries):
            try:
                self.send_sms(message)
                return
            except Exception as e:
                print(f"Error sending SMS: {str(e)}")

        print("Error sending SMS.")

class KavenegarService:
    def send_sms(self, message):
        # کد ارسال پیامک با استفاده از سرویس کاوه نگار
        print(f"Sending SMS via Kavenegar: {message}")

class SignalService:
    def send_sms(self, message):
        # کد ارسال پیامک با استفاده از سرویس سیگنال
        print(f"Sending SMS via Signal: {message}")

class User:
    def __init__(self, phone_number, circuit_breaker):
        self.phone_number = phone_number
        self.circuit_breaker = circuit_breaker

    def login(self):
        otp = random.randint(1000, 9999)  # generate a 4-digit OTP
        message = f"Your OTP is {otp}"
        self.circuit_breaker.send_sms(message)

# مثال استفاده از کد
kavenegar = KavenegarService()
signal = SignalService()

services = [kavenegar, signal]
breaker = CircuitBreaker(services, max_errors=3, cooldown_time=1800)

user = User(phone_number="09123456789", circuit_breaker=breaker)

# ورود به سیستم با استفاده از OTP
user.login()
