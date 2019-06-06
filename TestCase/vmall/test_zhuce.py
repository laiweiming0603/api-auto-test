from Common import Request,Assert,read_excel,Tools
import pytest,allure

tool_pwd = Tools.random_str_abc(3) + str(Tools.random_123(3))
tool_username = Tools.random_str_abc(3) + str(Tools.random_123(1))
tool_phone=Tools.phone_num()
request = Request.Request()
assertions = Assert.Assertions()
@allure.feature('注册模块')
class Test_zhuce:
    @allure.story('注册新用户')
    def test_zhuce(self):
        zhuce_resp = request.post_request(url='http://192.168.60.132:1811/user/signup',
                                            json={"phone": tool_phone, "pwd": tool_pwd, "rePwd": tool_pwd,
                                                  "userName":tool_username})
        assertions.assert_code(zhuce_resp.status_code,200)
        resp_json = zhuce_resp.json()
        assertions.assert_in_text(resp_json['respDesc'],'成功')
