import json

from flask      import Flask, jsonify, Response
from flask_cors import CORS
from flask.json import JSONEncoder
from decimal    import Decimal
from datetime   import datetime, date

class CustomJSONEncoder(JSONEncoder):
    """
    jsonify()를 사용하는데 몇몇 인코더가 필요한 부분이 있어서 obj : json 형태로 변환
    obj를 json형태로 변경하는 기능이 추가된 JSONEncoder
    """
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, bytes):
            return obj.decode("utf-8")
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        return JSONEncoder.default(self, obj)

    def create_app(test_config = None):
        """
        이름 : app = Flask(__name__)
        설명 : Flask 인스턴스를 생성
        설명2 : __name__는 파이썬 모듈의 이름이다. 앱은 실행 결로를 판단하기 위해
                해당 클래스를 호출한 모듈이 어딘지 알아야 하는데 __name__은 모듈을 지칭하는 편한 방법
        """
        app = Flask(__name__)

        app.json_encoder = CustomJSONEncoder
        """
        이름 : app.config.from_pyfile
        설명 : 기본 설정값을 인스턴스 폴더 내에 있는 config.py에 
               정의된 값으로 엎어쓴다.
        """
        app.config.from_pyfile('config.py')

        """
        CORS를 사용하고 *은 모두 접속 가능설정 
        """
        CORS(app, resources={'*': {'origins': '*'}}, expose_header='Authorization')