<template>
  <el-container>
      <el-header>
        <el-row :gutter="20">
        <el-menu 
          :default-active="'0'" 
          class="el-menu-demo" 
          mode="horizontal" 
          active-text-color="#000000"
          background-color = "#FFFFFF"
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
     <el-row>
      <el-col :span="12">
        <el-row><span  style="font-size:40px  ">打印详单</span></el-row>
        <div class = "rdrf">
          <el-form :model="rdrForm"  label-width="90px" ref="rdrForm" class="demo-ruleForm">
            <el-form-item label="房间号：" prop="roomId" :rules="[{ required: true, message: '房间号不能为空'},
            { type: 'number', message: '请输入数字', trigger: ['blur', 'change'] }]">
              <el-input type="text" v-model.number="rdrForm.roomId" width="100px"  autocomplete="off" placeholder="请输入房间号"></el-input>
            </el-form-item>
          </el-form>
          <div style="padding:10px">
              <el-button  @click="printf_rdr('rdrForm')" weight='50px' style="background-color:orange;color:white;width:100px">打印详单</el-button>
          </div>
        </div>
      </el-col>
      <el-col :span="12">
        <el-row><span  style="font-size:40px  ">打印账单</span></el-row>
        <div class = "rdrf">
          <el-form :model="invForm" label-width="90px" ref="invForm" class="demo-ruleForm">
            <el-form-item label="房间号：" prop="roomId" :rules="[{ required: true, message: '房间号不能为空'},
            { type: 'number', message: '请输入数字', trigger: ['blur', 'change'] }]">
              <el-input type="text" v-model.number="invForm.roomId" width="100px"  autocomplete="off" placeholder="请输入房间号"></el-input>
            </el-form-item>
          </el-form>
          <div style="padding:10px">
              <el-button  @click="printf_inv('invForm')" weight='50px' style="background-color:orange;color:white;width:100px">打印账单</el-button>
          </div>
        </div>
      </el-col>
     </el-row>
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
      return {
        url:'',
        roomId:'',
        rdrForm: {
          roomId: '',
        },
        invForm: {
          roomId: '',
        },
      }
    },
    created(){
      this.init();
    },
    mounted(){
        
    },
    methods:{
      init(){
        this.url = sessionStorage.getItem("url")
        this.roomId = sessionStorage.getItem("roomId")
      },
      to_home(){
        this.$router.push('/');
      },
      printf_rdr(formName){
        this.$refs[formName].validate((valid) => {
          if (valid) {
            let sent = {
              room_id : this.rdrForm.roomId,
            }
            this.$ajax({
              type: 'HEAD',
              method: 'post',
              url: this.url+'/desk/print_rdr/',
               withCredentials: true,
              crossDomain:true,
              changeOrigin: true,
              responseType: 'blob',
              data : sent
            })
            .then((response) => {    
              if(response.status == 200){
                const content = response
                const blob = new Blob([response.data])
                const fileName = this.rdrForm.roomId+'_详单.csv'
                if ('download' in document.createElement('a')) { // 非IE下载
                  const elink = document.createElement('a')
                  elink.download = fileName
                  elink.style.display = 'none'
                  elink.href = URL.createObjectURL(blob)
                  document.body.appendChild(elink)
                  elink.click()
                  URL.revokeObjectURL(elink.href) // 释放URL 对象
                  document.body.removeChild(elink)
                  } else { // IE10+下载
                    navigator.msSaveBlob(blob, fileName)
                  }
              }
            })
            .catch((error) => {
              
               this.$message.error(error.response.data.message);
            })
          } else {
            this.$message.error('请检查输入是否正确！');
            return false;
          }
        });
      },
      printf_inv(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            let sent = {
               room_id : this.invForm.roomId,
            }
            this.$ajax({
              type: 'HEAD',
              method: 'post',
              url: this.url+'/desk/print_invoice/',
               withCredentials: true,
              crossDomain:true,
              changeOrigin: true,
              data : sent
            })
            .then((response) => {    
              if(response.status == 200){
                const content = response
                const blob = new Blob([response.data])
                const fileName = this.invForm.roomId+'_账单.csv'
                if ('download' in document.createElement('a')) { // 非IE下载
                  const elink = document.createElement('a')
                  elink.download = fileName
                  elink.style.display = 'none'
                  elink.href = URL.createObjectURL(blob)
                  document.body.appendChild(elink)
                  elink.click()
                  URL.revokeObjectURL(elink.href) // 释放URL 对象
                  document.body.removeChild(elink)
                  } else { // IE10+下载
                    navigator.msSaveBlob(blob, fileName)
                  }
              }
            })
            .catch((error) => {
               this.$message.error(error.response.data.message);
            })
          } else {
            this.$message.error('请检查输入是否正确！');
            return false;
          }
        });
      }
    }
    
 };

</script>

<style scoped>
  .rdrf{
    border-radius: 15px;
    line-height: 16px;
    position: relative;
    left: 20%;
    width: 400px;
    height: 100px;
    padding: 15px;
    text-align:center;
    background:rgba(255,255,255,0.9);
  }
  .el-row {
    margin-bottom: 20px;
    &:last-child {
      margin-bottom: 0;
    }
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
