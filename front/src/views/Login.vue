<template>
  <el-container>
      <el-header>
        <el-row :gutter="20">
        <el-menu 
          :default-active="'0'" 
          class="el-menu-demo" 
          mode="horizontal" 
          active-text-color="#000000"
          background-color = "#005CAF"
        >
          <el-col :span="9" :offset="1"><pre></pre></el-col>

          <el-menu-item index="0" @click="to_home">
            <span class="iconfont">&#xe61e;</span>
          ACC空调管理系统
          </el-menu-item>
       </el-menu>
      </el-row>
    </el-header>
    <el-main>
      <div class = "logf">
        <span>登录</span>
        <el-form :model="logForm"  ref="logForm" class="demo-ruleForm">
          <el-form-item label="邮箱：" prop="username" :rules="[{ required: true, message: '账号不能为空'},]">
            <el-input type="text" v-model="logForm.username" autocomplete="off" placeholder="请输入账号"></el-input>
          </el-form-item>
          <el-form-item label="密码：" prop="password" :rules="[{ required: true, message: '密码不能为空'}]">
            <el-input type="password"  v-model="logForm.password" autocomplete="off" placeholder="请输入密码"></el-input>
          </el-form-item>
            <el-radio-group v-model="logForm.status">
                <el-radio :label="1">客房</el-radio>
                <el-radio :label="2">经理</el-radio>
                <el-radio :label="3">前台</el-radio>
                <el-radio :label="4">管理员</el-radio>
            </el-radio-group>
        </el-form>
        <div style="padding:10px">
            <el-button  @click="submitForm('logForm')" weight='50px' style="background-color:orange;color:white;width:100px">登录</el-button>
        </div>
      </div>
    </el-main>
   
  </el-container>

</template>

<script>
import Myfooter from '@/components/myfooter.vue'
import userHeader from '@/components/userheader.vue'
  export default {
    name:'login',
    components: { 
     userHeader,
     Myfooter,
    },
    data() {
      var checkusername = (rule, value, callback) => {
        if (!value) {
          return callback(new Error('账号不能为空'));
        } else {
          callback();
        }
      };
      var checkpass = (rule, value, callback) => {
       if (value === '') {
         callback(new Error('请输入密码'));
       } else {
         callback();
       }
     };
      return {
        publickey:'',
        logForm: {
         username: '',
         password: '',
         status:''
       },
       rules: {
         username: [
           { validator: checkusername, trigger: 'blur' }
         ],
         password: [
           { validator: checkpass, trigger: 'blur' }
         ]
       }
      }
    },
    
    mounted(){
        
    },
    methods:{
      to_home(){
        this.$router.push('/')
      },
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            let sent = {
              email : this.logForm.username,
              passwd :this.logForm.password,
              status:this.logForm.status
            }
            this.$ajax({
              type: 'HEAD',
              method: 'post',
              url: '/api/session',
              data : sent
            })
            .then((response) => {    
              //console.log(response)
              if(response.status == 200){
                if(response.data.result.accountType=='用户'){
                  sessionStorage.setItem("userType",this.logForm.status)
                  sessionStorage.setItem("userName",this.logForm.username)
                  //console.log( this.$store.getters.get_userlevel)

                }else {
                  //alert("请使用普通用户账号登录！
                } 
              }
            })
            .catch((error) => {
               //console.log(error.response)
               this.$message.error(error.response.data.message);
              //  alert(error.response.data.message)
            })
          } else {
            //console.log('error submit!!');//表单错误
            this.$message.error('请检查输入是否正确！');
            return false;
          }
        });
      }
    }
    
 };

</script>

<style scoped>
  .logf{
    border-radius: 15px;
    line-height: 16px;
    position: relative;
    width: 400px;
    height: 260px;
    top :50px;
    right:38%;
    float: right;
    padding: 15px;
    text-align:center;
    background:rgba(255,255,255,0.9);
  }
  .body {
    min-height: 100%;
    margin: 0;
    padding: 0;
    position: relative;
  }
  .el-main {
    color: #333;
    text-align: center;
    background: url(../images/homebg1.jpg);
    background-size: 100% 100%;
    width: 100%;
    height: 100%;
    left:-2px;
    top: 70px;
    bottom: 20px;
    position: fixed;
  }
  .el-header{
      color: rgb(91, 170, 180);
  }
  .el-footer {
    color:white;
    text-align: center;
    position: absolute;
    bottom: 0;
    width: 100%;
    height: 100%;
  }

</style>
