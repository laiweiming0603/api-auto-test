from Common import Request,Assert,read_excel,Login
import allure,pytest

request = Request.Request()
assertions = Assert.Assertions()
head=Login.Login().get_token()
url=Login.url
yhq_id=0
excel_list = read_excel.read_excel_list('./document/优惠券.xlsx')
ids_list=[]
for i in range(len(excel_list)):
    ids_list.append(excel_list[i].pop())

@allure.feature('优惠券模块')
class Test_yhq:
    @allure.story('获取优惠券列表')
    def test_yhq_sel(self):
        sel_resp = request.get_request(url=url+'coupon/list',
                                          params={"pageNum": 1, "pageSize": 10}, headers=head)
        assertions.assert_code(sel_resp.status_code,200)
        sel_resp_json = sel_resp.json()
        assertions.assert_in_text(sel_resp_json['message'],'成功')
        sel_resp_json_data = sel_resp_json['data']
        sel_resp_json_data_list = sel_resp_json_data['list']
        resp_json_dict= sel_resp_json_data_list[0]
        global yhq_id
        yhq_id=resp_json_dict['id']
    @allure.story('删除优惠券')
    def test_del(self):
        del_resp = request.post_request(url=url+'coupon/delete/' + str(yhq_id), headers=head)
        assertions.assert_code(del_resp.status_code,200)
        resp_json = del_resp.json()
        assertions.assert_in_text(resp_json['message'],'成功')
    @allure.story('添加优惠券')
    @pytest.mark.parametrize('name,amount,minPoint,publishCount,msg',excel_list,ids=ids_list)
    def test_add(self,name,amount,minPoint,publishCount,msg):
        add_resp = request.post_request(url=url+'coupon/create',
                                          json={"type":0,"name":name,"platform":0,"amount":amount,"perLimit":1,"minPoint":minPoint,"startTime":"","endTime":"","useType":0,"note":"","publishCount":publishCount,"productRelationList":[],"productCategoryRelationList":[]}, headers=head)
        assertions.assert_code(add_resp.status_code,200)
        resp_json = add_resp.json()
        assertions.assert_in_text(resp_json['message'],msg)



