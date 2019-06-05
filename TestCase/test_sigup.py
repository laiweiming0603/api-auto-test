from Common import Request,Assert,read_excel
import pytest,allure

request = Request.Request()
assertions = Assert.Assertions()
excel_list = read_excel.read_excel_list('./document/新用户注册.xlsx')
ids_list=[]
for i in range(len(excel_list)):
    ids_list.append(excel_list.pop())

@allure.feature('注册模块')
class Test_new:
    @allure.feature('注册新用户')
    @pytest.mark.parametrize('phone,pwd,rePwd,userName,msg',excel_list,ids=ids_list)
    def test_zhuce(self,phone,pwd,rePwd,userName,msg):
        zhuce_resp = request.post_request(url='http://192.168.60.132:1811/user/signup',
                                            json={"phone": phone, "pwd": pwd, "rePwd": rePwd,
                                                  "userName": userName})
        assertions.assert_code(zhuce_resp.status_code,200)
        resp_json = zhuce_resp.json()
        assertions.assert_in_text(resp_json['respDesc'],msg)
