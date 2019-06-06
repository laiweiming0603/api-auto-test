from Common import Request,Assert,read_excel,Tools
import pytest,allure

request = Request.Request()
assertions = Assert.Assertions()
excel_list = read_excel.read_excel_list('../../document/注册用例.xlsx')
ids_list=[]
for i in range(len(excel_list)):
    ids_list.append(excel_list[i].pop())
tool_pwd = Tools.random_str_abc(3) + Tools.random_123(3)
tool_username = Tools.random_str_abc(3) + Tools.random_123(1)
tool_phone=Tools.phone_num()

@allure.feature('注册模块')
class Test_new:
    @allure.story('注册新用户_成功')
    @pytest.mark.zhuce
    def test_zhuce(self):
        zhuce_resp = request.post_request(url='http://192.168.60.132:1811/user/signup',
                                          json={"phone": tool_phone, "pwd": tool_pwd, "rePwd": tool_pwd,
                                                "userName": tool_username})
        assertions.assert_code(zhuce_resp.status_code, 200)
        resp_json = zhuce_resp.json()
        assertions.assert_in_text(resp_json['respDesc'], '成功')


    @allure.story('注册新用户_失败')
    @pytest.mark.parametrize('phone,pwd,rePwd,userName,code',excel_list,ids=ids_list)
    @pytest.mark.zhuce
    def test_zhuce(self,phone,pwd,rePwd,userName,code):
        zhuce_resp = request.post_request(url='http://192.168.60.132:1811/user/signup',
                                            json={"phone": phone, "pwd": pwd, "rePwd": rePwd,
                                                  "userName": userName})
        assertions.assert_code(zhuce_resp.status_code,200)
        resp_json = zhuce_resp.json()
        assertions.assert_in_text(resp_json['respCode'],code)
