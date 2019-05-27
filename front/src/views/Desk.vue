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
     
    </el-main>
   
  </el-container>

</template>

<script>
import Myfooter from '@/components/myfooter.vue'
import userHeader from '@/components/userheader.vue'
  export default {
    name:'Desk',
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
