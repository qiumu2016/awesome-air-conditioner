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

          <el-menu-item index="0" >
            <span class="iconfont">&#xe61e;</span>
          ACC空调管理系统
          </el-menu-item>
       </el-menu>
      </el-row>
    </el-header>
    <el-main>
     <el-row>
      <el-col :span="12"><el-row><span  style="font-size:40px  ">显示</span></el-row>
        <el-col :span="12">
          <div class = "current"><el-row><span  style="font-size:20px">实时信息</span></el-row>
            <el-row><span class = "text">是否入住：{{isCheckIn}}</span></el-row>
            <el-row><span class = "text">是否开机：{{isOpen}}</span></el-row>
            <el-row><span class = "text">是否服务：{{isServing}}</span></el-row>
            <el-row><span class = "text">当前风速：{{cur_wind}}</span></el-row>
            <el-row><span class = "text">当前温度：{{cur_temp}}℃</span></el-row>
            <el-row><span class = "text">当前费率：{{fee_rate}}</span></el-row>
            <el-row><span class = "text">当前费用：{{fee}}</span></el-row>
          </div>
        </el-col>
        <el-col :span="12">
          <div class = "setting"><el-row><span  style="font-size:20px">设定信息</span></el-row>
            <el-row><span class = "text">是否开机：{{ispower}}</span></el-row>
            <el-row><span class = "text">当前模式：{{model}}</span></el-row>
            <el-row><span class = "text">室外温度：{{outdoor}}℃</span></el-row>
            <el-row><span class = "text">设定温度：{{set_temp}}℃</span></el-row>
            <el-row><span class = "text">设定风速：{{set_wind}}</span></el-row>
          </div>
        </el-col>
      </el-col>
      <el-col :span="12"><el-row><span  style="font-size:40px">遥控</span></el-row>
                         <div class="controler"> 
                          <el-row :gutter="40">
                            <el-button type="success" style = "width:120px" @click="request_on()">开机</el-button>
                            <el-button type="danger" style = "width:120px" @click="request_off()">关机</el-button>
                          </el-row>
                          <el-row :gutter="40">
                            <el-button type="primary" style = "width:120px" @click="temp_inc()">温度 +</el-button>
                            <el-button type="primary" style = "width:120px" @click="temp_dec()">温度 -</el-button>
                          </el-row>
                          <el-row :gutter="40">
                             <el-button type="warning" style = "width:75px" @click="wind_change(0)">弱风</el-button>
                             <el-button type="warning" style = "width:75px" @click="wind_change(1)">中风</el-button>
                             <el-button type="warning" style = "width:75px" @click="wind_change(2)">强风</el-button>
                          </el-row>
                         </div>
      </el-col>
    </el-row>
    <el-row>
       <el-col :span="8">
       </el-col>
       <el-col :span="8">
         <div class="image"> 
           <img v-show="ispower == '已开机'" :src = "img1.src" height="180" width="550">
           <img v-show="ispower == '未开机'" :src = "img2.src" height="180" width="550">
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
var InitSetInterval
var changeT
  export default {
    name:'Costumer',
    components: { 
     userHeader,
     Myfooter,
    },
    data() {
      return {
       url:'',
       img1:{id:1, src:require('../images/power.gif')},
       img2:{id:2, src:require('../images/power1.jpeg')},
       roomId:'',
       set_temp:24,
       model:'制冷',
       cur_temp:'',
       set_wind:'弱风',
       wind:'low',
       cur_wind:'',
       ispower:'未开机',
       isCheckIn:'未入住',
       isOpen:'未开机',
       isServing:'未在服务',
       wind:['弱风','中风','强风'],
       winden:['low','mid','high'],
       fee_rate:'',
       fee:'',
       maxt:'',
       mint:'',
       checkin:['未入住','已入住'],
       open:['未开机','已开机'],
       serve:['正在服务','未在服务'],
       outdoor:30,
      }
    },
    created(){
      InitSetInterval = setInterval(this.request_info(),1000)
      this.init();
    },
    mounted(){
        
    },
    destroyed() {
      clearInterval(InitSetInterval)
    },
    methods:{
      init(){
        this.cur_temp = this.outdoor
        this.url = sessionStorage.getItem("url")
        this.roomId = sessionStorage.getItem("roomId")
      },
      changtemp(){
        if(this.ispower =='未开机'){
           if(this.model == '制冷' &&this.cur_temp < this.outdoor){
              this.cur_temp = this.cur_temp + 0.5
            }else if(this.model == '制暖' && this.cur_temp > this.outdoor){
              this.cur_temp = this.cur_temp - 0.5
            }
            if(this.model == '制冷' && this.cur_temp > (this.set_temp+1)){
              window.clearInterval(changeT); 
              this.request_on()
            }
            if(this.model == '制暖' && this.cur_temp < (this.set_temp-1)){
              window.clearInterval(changeT); 
              this.request_on()
            }
        }
       
      },
      request_info(){
        let sent = {
              room_id :this.roomId,
            }
          this.$ajax({
              type: 'HEAD',
              method: 'post',
              url: this.url+'/customer/request_info/',
               withCredentials: true,
              crossDomain:true,
              changeOrigin: true,
              data : sent
            })
            .then((response) => {    
              if(response.status == 200){
                this.isCheckIn = this.checkin[response.isCheckIn]
                this.isOpen = this.open[response.isOpen]
                this.ispower = this.open[response.isOpen]
                this.isServing = this.serve[response.isServing]
                this.cur_wind = response.wind = 'high'?'强风':response.wind = 'mid'?'中风':'弱风'
                this.cur_temp = response.current_temp
                this.fee_rate = response.fee_rate
                this.fee = response.fee
                if(this.ispower == '未开机'){
                  changeT = window.setInterval(this.changtemp(),1000); 
                }
              }
            })
            .catch((error) => {
               this.$message.error(error.response.message);
            })
      },
      request_on(){
        if(this.ispower == '已开机'){
          this.$message({
            message: '已开机！',
            type: 'warning'
          });
        } else if(this.ispower == '未开机'){
           let sent = {
              room_id :this.roomId,
              current_room_temp :this.cur_temp
            }
          this.$ajax({
              type: 'HEAD',
              method: 'post',
              url: this.url+'/customer/request_on/',
               withCredentials: true,
              crossDomain:true,
              changeOrigin: true,
              data : sent
            })
            .then((response) => {    
              if(response.status == 200){
                this.model = response.model = 'cold'?'制冷':'制暖'
                this.set_temp = response.target_temp
                this.maxt = response.temp_high_limit
                this.mint = response.temp_low_limit
                this.ispower = '已开机'
                this.isOpen = '已开机'
              }
            })
            .catch((error) => {
               this.$message.error(error.response.message);
            })
          
        }
        
      },
      request_off(){
        if(this.ispower == '未开机'){
          this.$message({
            message: '未开机！',
            type: 'warning'
          });
        } else if(this.ispower == '已开机'){
           let sent = {
              room_id :this.roomId,
              current_room_temp :this.cur_temp
            }
          this.$ajax({
              type: 'HEAD',
              method: 'post',
              url: this.url+'/customer/request_off/',
               withCredentials: true,
              crossDomain:true,
              changeOrigin: true,
              data : sent
            })
            .then((response) => {    
              if(response.status == 200){
                this.ispower = '未开机'
                this.isOpen = '未开机'
                changeT = window.setInterval(this.changtemp(),1000); 
              }
            })
            .catch((error) => {
               this.$message.error(error.response.message);
            })
        }
      },
      temp_inc(){
        if(this.ispower == '已开机'){
         if(this.set_temp+1 > this.maxt){
            this.$message({
            message: '超出可设定温度上限！',
            type: 'warning'
          });
         }else {
           let sent = {
              room_id :this.roomId,
              target_temp :this.set_temp+1
            }
          this.$ajax({
              type: 'HEAD',
              method: 'post',
              url: this.url+'/customer/change_target_temp/',
               withCredentials: true,
              crossDomain:true,
              changeOrigin: true,
              data : sent
            })
            .then((response) => {    
              if(response.status == 200){
                this.set_temp++;
              }
            })
            .catch((error) => {
               this.$message.error(error.response.message);
            })
          }
        }else{
          this.$message({
            message: '未开机！',
            type: 'warning'
          });
        }
        
      },
      temp_dec(){
        if(this.ispower == '已开机'){
         if(this.set_temp-1 < this.maxt){
            this.$message({
            message: '超出可设定温度下限！',
            type: 'warning'
          });
         }else {
           let sent = {
              room_id :this.roomId,
              target_temp :this.set_temp-1
            }
          this.$ajax({
              type: 'HEAD',
              method: 'post',
              url: this.url+'/customer/change_target_temp/',
               withCredentials: true,
              crossDomain:true,
              changeOrigin: true,
              data : sent
            })
            .then((response) => {    
              if(response.status == 200){
                this.set_temp--;
              }
            })
            .catch((error) => {
               this.$message.error(error.response.message);
            })
          }
        }else{
          this.$message({
            message: '未开机！',
            type: 'warning'
          });
        }
      },
      wind_change(wind){
        if(this.ispower == '已开机'){
          if(this.set_wind !=this.wind[wind]){
             let sent = {
              room_id :this.roomId,
              fan_speed :this.winden[wind]
            }
          this.$ajax({
              type: 'HEAD',
              method: 'post',
              url: this.url+'/customer/change_fan_speed/',
               withCredentials: true,
              crossDomain:true,
              changeOrigin: true,
              data : sent
            })
            .then((response) => {    
              if(response.status == 200){
                this.set_wind = this.wind[wind]
              }
            })
            .catch((error) => {
               this.$message.error(error.response.message);
            })
          }
        }else{
          this.$message({
            message: '未开机！',
            type: 'warning' 
          });
        }
      },
    }
    
 };

</script>

<style scoped>
  .text{
    font-size:15px;
    position: relative;
    float: left;
    left:20%
  }
  .el-row {
    margin-bottom: 20px;
    &:last-child {
      margin-bottom: 0;
    }
  }
  .current{
    border-radius: 15px;
    line-height: 16px;
    position: relative;
    left: 12%;
    float: right;
    width: 300px;
    padding: 15px;
    text-align:center;
    background:rgba(255, 255, 255, 0.7);
  }
  .setting{
    left: 12%;
    float: right;
    border-radius: 15px;
    line-height: 16px;
    position: relative;
    width: 300px;
    padding: 15px;
    text-align:center;
    background:rgba(255, 255, 255, 0.7);
  }
  .image{
    border-radius: 15px;
    line-height: 16px;
    position: relative;
    left: 90%;
    width: 600px;
    height: 180px;
    padding: 15px;
    text-align:center;
    background:rgba(255, 255, 255, 0.7);
  }
  .controler{
    border-radius: 15px;
    line-height: 16px;
    position: relative;
    width: 400px;
    right:22%;
    float: right;
    padding: 15px;
    text-align:center;
    background:rgba(255, 255, 255, 0.7);
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
