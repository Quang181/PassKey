from .ports import InfoUserByTokenUseCase


class InfoUserByTokenService(InfoUserByTokenUseCase):
    def __init__(self):
        super().__init__()

    def get_info_user(self, info_user) -> dict:
        data_convert = {
            **info_user
        }
        return data_convert