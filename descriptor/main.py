class Value:
    def __init__(self):
        self.value = 0.0

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        # не сказано - должен ли дескриптор в конструкторе получать комиссию
        # или при установке значения, поэтому это вариант - при установке.
        # архитектурно - выглядит плохо, но позволяет менять комиссию "на лету"
        assert hasattr(instance, 'commission'), "owner doesn't have attr \"commission\""
        self.value = value - value * instance.commission

    def __delete__(self, instance):
        pass


class Account:
    amount = Value()

    def __init__(self, commission):
        self.commission = commission


class AccountNoCommission:
    amount = Value()

    def __init__(self):
        pass


if __name__ == '__main__':
    new_account = Account(0.1)
    new_account.amount = 100

    print(new_account.amount)
