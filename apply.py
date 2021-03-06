from oa import OA
from config import users


def apply_all() -> None:
    for user in users:
        print()
        obj = OA(user)
        obj.login()
        obj.login_oa()
        obj.apply()
    print()


if __name__ == '__main__':
    apply_all()
