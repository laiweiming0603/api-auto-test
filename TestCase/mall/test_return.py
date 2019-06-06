from Common import Request,Assert,read_excel,Login
import allure,pytest
head=Login.Login().get_token()
request = Request.Request()
assertions = Assert.Assertions()
url=Login.url
th_id=0
excel_list = read_excel.read_excel_list('./document/退货.xlsx')
ids_list=[]
for i in range(len(excel_list)):
    ids_list.append(excel_list[i].pop())

@allure.feature('退货模块')
class Test_return:
    @allure.story('获取退货列表')
    def test_sel(self):
        sel_resp = request.get_request(url=url+'returnReason/list',
                                          params={'pageNum': 1, 'pageSize': 5}, headers=head)
        assertions.assert_code(sel_resp.status_code,200)
        sel_resp_json = sel_resp.json()
        assertions.assert_in_text(sel_resp_json['message'],'成功')
        json_data = sel_resp_json['data']
        data_list = json_data['list']
        data_list_item = data_list[0]
        global th_id
        th_id=data_list_item['id']
    @allure.story('删除退货原因')
    def test_del(self):
        del_resp = request.post_request(url=url + 'returnReason/delete' ,params={'ids':str(th_id)}, headers=head)
        assertions.assert_code(del_resp.status_code, 200)
        del_resp_json = del_resp.json()
        assertions.assert_in_text(del_resp_json['message'], '成功')
    @allure.story('添加退货原因')
    @pytest.mark.parametrize('name,sort,status,msg',excel_list,ids=ids_list)
    def test_add(self,name,sort,status,msg):
        add_resp = request.post_request(url=url + 'returnReason/create',
                                            json={"name": name, "sort": sort, "status": status, "createTime": ""}, headers=head)
        assertions.assert_code(add_resp.status_code, 200)
        add_resp_json = add_resp.json()
        assertions.assert_in_text(add_resp_json['message'], msg)