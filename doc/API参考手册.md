# API参考手册

本系统所有的API均按照RESTful风格进行设计，返回的格式均为`JSON`数据。对于所有**POST**请求(特别说明的除外)，提交的表单应为`JSON`格式，请求的`header`的`Content-Type`字段应当为`application/json`。所有API的返回数据均包含`message`字段，当请求被正确相应时，`message`字段的值为`OK`；若请求有数据返回时，除`message`字段外，还有`result`字段，为被请求的内容；当请求未被相应或发生异常时，`message`字段通常包含了详细的错误信息。

处理返回的消息时，请尽量避免通过判断`message`是否为`OK`来确定请求是否成功相应，而应当根据返回的消息头内的HTTP状态码来判断。

##认证

### 创建会话(登录)

**URL**

`POST /session`

<br/>

**描述**

向服务器提交用户名和密码，获取认证凭证用于后续访问

<br/>

**请求参数**

```json
{
    "name": "310E", 	//房间号码/前台员工账号/经理账号/管理员账号，作为登录名和用户唯一标识
    "passwd": "admin"	//管理员设置的房间从机登录密码
}
```

<br/>

**请求结果**

```json
{
    "message": "OK",
    "result": {
        "accountType": "用户"			//表示账户类型：用户/管理员/经理/前台
    }
}
```

*注意返回消息的Headers里面有`Set-Cookie`字段，请按要求设置cookie，该cookie将作为后续请求的身份标识*

<br/>