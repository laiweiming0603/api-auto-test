from Common import Request,Assert,read_excel
import allure,pytest,json

request = Request.Request()
assertions = Assert.Assertions()

head={}
fenlei_id=0

excel_list = read_excel.read_excel_list('./document/添加商品分类.xlsx')
ids_list=[]
for i in range(len(excel_list)):
    ids_pop = excel_list[i].pop()
    ids_list.append(ids_pop)

@allure.feature('商品分类模块')
class Test_info:
    @allure.story('登录接口')
    def test_login(self):
        login_resp = request.post_request(url='http://192.168.60.132:8080/admin/login',
                                            json={"username": "admin", "password": "123456"})
        assertions.assert_code(login_resp.status_code,200)
        login_resp_json = login_resp.json()
        assertions.assert_in_text(login_resp_json['message'],'成功')
        #提取token
        data_json = login_resp_json['data']
        json_token = data_json['tokenHead'] + data_json['token']
        global head
        head={'Authorization':json_token}
    @allure.story('获取商品分类')
    def test_sel(self):
        sel_resp = request.get_request(url='http://192.168.60.132:8080/productCategory/list/0',params={'pageNum':1,'pageSize':5}, headers=head)
        assertions.assert_code(sel_resp.status_code, 200)
        sel_resp_json = sel_resp.json()
        assertions.assert_in_text(sel_resp_json['message'], '成功')
        sel_resp_json_data = sel_resp_json['data']
        sel_resp_json_data_list = sel_resp_json_data['list']
        fenlei_dict = sel_resp_json_data_list[0]
        global fenlei_id
        fenlei_id=fenlei_dict['id']
    @allure.story('删除商品分类')
    def test_del(self):
        del_resp = request.post_request(url='http://192.168.60.132:8080/productCategory/delete/' + str(fenlei_id),
                                          headers=head)
        assertions.assert_code(del_resp.status_code, 200)
        del_resp_json = del_resp.json()
        assertions.assert_in_text(del_resp_json['message'], '成功')



    @allure.story('添加商品分类')
    def test_insert(self):
        insert_resp = request.post_request(url='http://192.168.60.132:8080/productCategory/create',
                                           json={"description":"","icon":"","keywords":"",
                                                "name":"咸鱼突刺","navStatus":0,"parentId":0,"productUnit":"","showStatus":0,"sort":0,"productAttributeIdList":[]}
                                            ,headers=head)
        assertions.assert_code(insert_resp.status_code, 200)
        insert_resp_json = insert_resp.json()
        assertions.assert_in_text(insert_resp_json['message'], '成功')




    @allure.story('添加商品分类参数化')
    @pytest.mark.parametrize('description,icon,keywords,name,navStatus,parentId,productUnit,showStatus,sort,productAttributeIdList,msg',excel_list,ids=ids_list)
    def test_add(self,description,icon,keywords,name,navStatus,parentId,productUnit,showStatus,sort,productAttributeIdList,msg):
        insert_resp = request.post_request(url='http://192.168.60.132:8080/productCategory/create',
                                           json={"description": description, "icon": icon, "keywords":keywords,
                                                 "name": name, "navStatus": navStatus, "parentId": parentId, "productUnit": productUnit,
                                                 "showStatus": showStatus, "sort": sort, "productAttributeIdList": [productAttributeIdList]}
                                           , headers=head)
        assertions.assert_code(insert_resp.status_code, 200)
        insert_resp_json = insert_resp.json()
        assertions.assert_in_text(insert_resp_json['message'],msg)
