import json
import urllib.parse

import requests


class TelegramBot:
    def __init__(self, token) -> None:
        self.token = token
        self.url = f'https://api.telegram.org/bot{self.token}'
        self.verify = self.auth()

    def auth(self):
        url = f'{self.url}/getMe'
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            print('authentication success!')
            return True
        elif r.status_code == 401:
            print('invalid token')
            return False
        elif r.status_code != 200:
            print(
                f'authentication error! response: {r.json()}')
            return False
        else:
            print(
                f'unknown error, response: {r.json()}')
            return False

    def send_message(
            self,
            chat_id: list,
            message: str,
            block_code: bool = False,
            r_status_code=True,
            print_log='message',
            reply=None):
        response_return = []
        message = urllib.parse.quote_plus(message)
        for id in chat_id:
            method = f'/sendMessage?chat_id={id}&text={message}' \
                '&protect_content=True&parse_mode=Markdown&disable_web_page_preview=True'
            if block_code is True:
                method = f'/sendMessage?chat_id={id}&text=`{message}`' \
                    '&protect_content=True&parse_mode=MarkdownV2'
            if reply:
                method += f'&reply_to_message_id={reply}'
            r = requests.post(f'{self.url}{method}', timeout=5)
            if r_status_code is True:
                print(f'message sent: {print_log} - {r.status_code}')
            else:
                print(f'message sent: {print_log}')
            if r.status_code != 200:
                print(r.json())
            response_return.append({'chat_id': id, 'response': r.json()})
        return response_return

    def send_image(self, chat_id: list, image_path: str, text=None, print_log='image'):
        results: list = []
        for id in chat_id:
            try:
                files = {'photo': open(image_path, 'rb')}
                if text:
                    data = {'chat_id': id,
                            'caption': text, 'parse_mode': 'Markdown'}
                else:
                    data = {'chat_id': id}
                method = f'{self.url}/sendPhoto'
                r = requests.post(method, files=files, data=data)
                print(f'image sent: {print_log} - {r.status_code}')
                if r.status_code != 200:
                    print(r.json())
            except Exception as error:
                print(
                    f'unexpected error {error} - r.json()')
            finally:
                results.append(r.json())
        return results

    def send_sticker(self, chat_id: list, sticker_id: str, print_log='sticker'):
        results: list = []
        for id in chat_id:
            try:
                url = f"https://api.telegram.org/bot{self.token}/sendSticker"
                data = {'chat_id': id, 'sticker': sticker_id}
                r = requests.post(url, data=data)
                print(f'image sent: {print_log} - {r.status_code}')
                if r.status_code != 200:
                    print(r.json())
            except Exception as error:
                print(
                    f'unexpected error {error} - r.json()')
            finally:
                results.append(r.json())
        return results

    def send_button(self, chat_id: list, text: str, keyboard: dict, print_log='button'):
        """
        keyboard example: {"text": "Link", "url": "https://www.google.com"}
        """
        method = f"{self.url}/sendMessage"
        results: list = []
        for chat in chat_id:
            try:
                buttons = json.dumps({'inline_keyboard': [[keyboard]]})
                payload = {"chat_id": chat, "text": text,
                           "reply_markup": buttons, "parse_mode": "Markdown"}
                r = requests.post(method, json=payload)
                print(f'button sent: {print_log} - {r.status_code}')
                if r.status_code != 200:
                    print(r.json())
            except Exception as error:
                print(
                    f'unexpected error {error} - r.json()')
            finally:
                results.append(r.json())
        return results
