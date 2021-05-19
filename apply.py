from oa import OA
from config import users


def apply_all() -> None:
    oa = OA(users[0])
    oa.launch()
    for user in users:
        print()
        oa.update_config(user)
        oa.login()
        oa.apply()
        oa.logout()
    print()
    oa.quit()


if __name__ == '__main__':
    apply_all()
