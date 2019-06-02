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

          <el-menu-item index="0"  @click="to_home">
            <span class="iconfont">&#xe61e;</span>
          ACC空调管理系统
          </el-menu-item>
       </el-menu>
      </el-row>
    </el-header>
    <el-main>
     <el-row>
        <el-col :span="8">
        </el-col>
        <el-col :span="8">
          <div class = "f">
             <el-radio v-model="radio" label="0">日报表</el-radio>
             <el-radio v-model="radio" label="1">周报表</el-radio>
             <el-radio v-model="radio" label="2">月报表</el-radio>
             <el-radio v-model="radio" label="3">年报表</el-radio>
            <div style="padding:10px">
              <el-button  @click="printf_report()" weight='50px' style="background-color:orange;color:white;width:100px">打印报表</el-button>
            </div>
          </div>
        </el-col>
        <el-col :span="8">
        </el-col>
     </el-row>
    </el-main>
   
  </el-container>

</template>

<script>
import Myfooter from '@/components/myfooter.vue'
import userHeader from '@/components/userheader.vue'
  export default {
    name:'Costumer',
    components: { 
     userHeader,
     Myfooter,
    },
    data() {
      return{
        url:'',
        roomId:'',
        radio: '0'
      }
    },
    created(){
      this.init();
    },
    
    methods:{
      init(){
        this.url = sessionStorage.getItem("url")
        this.roomId = sessionStorage.getItem("roomId")
      },
      to_home(){
        this.$router.push('/');
      },
      printf_report(){
        let sent = {
              type : this.radio,
            }
          this.$ajax({
              type: 'HEAD',
              method: 'post',
              url: this.url+'/manager/print_report/',
               withCredentials: true,
              crossDomain:true,
              changeOrigin: true,
              data : sent
            })
            .then((response) => {    
              if(response.status == 200){
          
              }
            })
            .catch((error) => {
              
               this.$message.error(error.response.message);
            })
        }
    }
    
 };

</script>

<style scoped>
  .f{
    border-radius: 15px;
    line-height: 16px;
    position: relative;
    top:100px;
    left: 100%;
    width: 400px;
    height: 60px;
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
