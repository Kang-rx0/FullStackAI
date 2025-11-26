frontend-src-views-Login：
    登录界面设计表单Form。表单自带rules属性，即可以设置校验规则（如必填等）。这里用了element plus的
FormInstance, FormRules。
    把表单对象的节点设置为FormInstance类型，校验规则设置为FormRules类型。
    把规则rules设置为FormRules类型，并且设置required为True，表示必填项。
调用formRef.value.validate方法进行表单校验。validate方法接收一个回调函数作为参数，回调函数的参数valid表示校验是否通过（element puls自动生成）。
    
    如果校验通过，则调用loginAPI发送登录请求；如果校验不通过，则使用ElMessage显示错误信息。
    --- loginAPI定义在frontend-src-api-user.ts中，使用axios发送POST请求到后端的登录接口。
    --- loginAPI里用到的request是frontend-src-utils-request.ts中定义的axios实例，已经配置了baseURL和请求拦截器等。

frontend-src-api-user：
    定义了loginAPI函数，接收用户名和密码作为参数，发送POST请求到后端的登录接口/api/v1/auth/login。
    使用request实例发送请求，request实例已经配置了baseURL和请求拦截器等。

frontend-src-api-request：
    创建了一个axios实例request，配置了baseURL为环境变量VITE_API_BASE_URL（在.env文件中设置）。
    配置了请求拦截器，可以在请求发送前添加token等信息。