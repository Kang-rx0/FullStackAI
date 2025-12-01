frontend-src-views-Login：
    登录界面设计表单Form。表单自带rules属性，即可以设置校验规则（如必填等）。这里用了element plus的FormInstance, FormRules。

    把表单对象的节点设置为FormInstance类型，校验规则设置为FormRules类型。

    把规则rules设置为FormRules类型，并且设置required为True，表示必填项。调用formRef.value.validate方法进行表单校验。validate方法接收一个回调函数作为参数，回调函数的参数valid表示校验是否通过（element puls自动生成）。
    
    如果校验通过，则调用loginAPI发送登录请求；如果校验不通过，则使用ElMessage显示错误信息。
    --- loginAPI定义在frontend-src-api-user.ts中，使用axios发送POST请求到后端的登录接口。
    --- loginAPI里用到的request是frontend-src-utils-request.ts中定义的axios实例，已经配置了baseURL和请求拦截器等。

frontend-src-api-user：
    定义了loginAPI函数，接收用户名和密码作为参数，发送POST请求到后端的登录接口/api/v1/auth/login。
    使用request实例发送请求，request实例已经配置了baseURL和请求拦截器等。

frontend-src-api-request：
    创建了一个方法：request，用于在user.ts中发送HTTP请求。
  - request用了fetch函数来发送请求，并且定义了一个字典变量options来存储配置（method，headers等）。
  - options的类型是RequestInit，定义了 fetch 支持的所有参数（如 method、headers、body、credentials、mode 等）
  - config参数合并了写死的headers和传入的options参数。（没有必要config，直接在options里面写入headers会更灵活一点）


# 后端
backeend-app-models-user.py：
  

backend-app-schemas-auth.py：
    定义了登录请求和响应的Pydantic模型。

  - LoginRequest模型包含account和password字段，表示登录请求的数据结构。

  - AuthResponse模型包含message、token和user字段，表示登录响应的数据结构。不包含密码，`这取决于 backend-app-schemas-user.py 里的 UserInfor模型定义。然后又把UserInfor模型引入到AuthResponse模型里。略有些混乱`

**待修改**
前端输入账户和密码后，点击登录 --- 发账户和密码到后端 --- 后端接受，验证用户是否存在于数据库（用户名或者邮箱）；密码是否正确 --- 如果验证通过，生成JWT token，跟用户信息和成功消息一起返回给前端 --- 前端收到后，输出成功消息提示；把token存到localStorage里。  

`目前没有实现 token 存储到 localStorage 的逻辑，后续需要在前端代码里添加`
