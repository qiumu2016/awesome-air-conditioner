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
        <el-col :span="12"><el-row><span  style="font-size:40px ">操作面板</span></el-row>
          <div class = 'power_on'>
            <el-row><span  style="font-size:20px">主机信息</span></el-row>
            <el-row><span class = "text">是否开机：{{isPoweron}}</span></el-row>
            <el-row :gutter="40">
                            <el-button type="success" style = "width:120px" @click="power_on()">开机</el-button>
                            <el-button type="danger" style = "width:120px" @click="power_off()">关机</el-button>
                          </el-row>
          </div>
           <div class = 'set_p'>
             <el-form ref="form" :model="form" :rules="Rules" label-width="130px" size="mini">
                <el-form-item label="工作模式：">
                  <el-radio-group v-model="form.model">
                    <el-radio label="hot">制暖</el-radio>
                    <el-radio label="cold">制冷</el-radio>
                  </el-radio-group>
                </el-form-item>

                 <el-form-item label="温度区间：" >
                   <el-col  class="line" :span="8">
                     <el-form-item prop="mint"  :rules="[
                      { required: true, message: '最低温度不能为空'},
                      { type: 'number', message: '必须为数字值'}]">
                    <el-input v-model.number="form.mint"  @change ='changemint' >
                    </el-input>
                     </el-form-item>
                 </el-col>
                  <el-col class="line" :span="2">-</el-col>
                  <el-col  class="line" :span="14">
                  <el-form-item  prop="maxt" :rules="[
                      { required: true, message: '最高温度不能为空'},
                      { type: 'number', message: '必须为数字值'}]">
                  <el-input v-model.number="form.maxt"
                  @change ='changemaxt'>
                    <template slot="append">℃</template>
                  </el-input>
                  </el-form-item>
                  </el-col>
                </el-form-item>
                <el-form-item label="默认目标温度：" prop="target" :rules="[
                      { required: true, message: '最低温度不能为空'},
                      { type: 'number', message: '必须为数字值'}]">
                  <el-input v-model.number="form.target">
                    <template slot="append">℃</template>
                  </el-input>
                </el-form-item>
                <el-form-item label="高风速费率：" prop="fee_rate_h">
                  <el-input  v-model="form.fee_rate_h">
                    <template slot="append">元/分钟</template>
                  </el-input>
                </el-form-item>
                <el-form-item label="中风速费率：" prop="fee_rate_m">
                  <el-input v-model="form.fee_rate_m">
                    <template slot="append">元/分钟</template>
                  </el-input>
                </el-form-item>
                <el-form-item label="低风速费率：" prop="fee_rate_l">
                  <el-input v-model="form.fee_rate_l">
                    <template slot="append">元/分钟</template>
                  </el-input>
                </el-form-item>
                <el-form-item label="房间数：" prop="num_rooms">
                  <el-input-number v-model.number="form.num_rooms"
                  :precision='0' 
                  :min="1">
                  </el-input-number>
                </el-form-item>
                <el-form-item label="最大服务房间数：" prop="num_serve">
                  <el-input-number v-model.number="form.num_serve"
                  :precision='0'
                  :min="1">
                  </el-input-number>
                </el-form-item>
                <div style="padding:0px">
                  <el-button  @click="set_para('form')" weight='50px' style="background-color:orange;color:white;width:100px">设置参数</el-button>
                   <el-button :disabled='disabled' @click="start_up()" weight='50px' style="background-color:blue;color:white;width:100px">启动服务</el-button>
              </div>
             </el-form>
           </div>
        </el-col>
        <el-col :span="12"><el-row><span  style="font-size:40px">查看房间</span></el-row>
          <div class = "checkf">
          <el-form :model="checkForm" label-width="90px" ref="checkForm" class="demo-ruleForm">
            <el-form-item label="房间号：" prop="roomId" :rules="[{ required: true, message: '房间号不能为空'},
            { type: 'number', message: '请输入数字', trigger: ['blur', 'change'] }]">
              <el-input type="text" v-model.number="checkForm.roomId" width="100px"  autocomplete="off" placeholder="请输入房间号"></el-input>
            </el-form-item>
          </el-form>
          <div style="padding:10px">
              <el-button  @click="check('checkForm')" type="success" style = "width:120px">查看</el-button>
          </div>
        </div>
        <div class = 'room'><el-row><span  style="font-size:20px">客房信息</span></el-row>
           <el-row><span class = "text">是否入住：{{isCheckIn}}</span></el-row>
            <el-row><span class = "text">是否开机：{{isOpen}}</span></el-row>
            <el-row><span class = "text">是否服务：{{isServing}}</span></el-row>
            <el-row><span class = "text">当前风速：{{cur_wind}}</span></el-row>
            <el-row><span class = "text">当前温度：{{cur_temp}}℃</span></el-row>
            <el-row><span class = "text">目标温度：{{tar_temp}}℃</span></el-row>
            <el-row><span class = "text">当前费率：{{fee_rate}}</span></el-row>
            <el-row><span class = "text">当前费用：{{fee}}</span></el-row>
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
    name:'Costumer',
    components: { 
     userHeader,
     Myfooter,
    },
    data() {
      var regnum = /^([1-9][0-9]*)+(.[0-9]{1,2})?$/
      var check = (rule, value, callback) => {
         if (value ===""){
          callback(new Error('请输入数字！'))
        } else if(!regnum.test(value)){
            callback(new Error('请输入两位小数！'))
          } else {
            callback();
          }
      };
      return{
        url:'',
        roomId:'',
        disabled:true,
        isPoweron:'未开机',
        checkForm: {
         roomId: '',
       },
       isCheckIn:'未入住',
       isOpen:'未开机',
       isServing:'未服务',
       cur_wind:'',
       cur_temp:'',
       tar_temp:'',
       fee_rate:'',
       fee:'',
       chechen:['未入住','已入住'],
       open:['未开机','已开机'],
       serving:['未服务','已服务'],
        form:{
          model:'cold',
          mint:20,
          maxt:30,
          target:24,
          fee_rate_h:1,
          fee_rate_m:0.5,
          fee_rate_l:0.3,
          num_rooms:5,
          num_serve:3,
        },
      Rules:{
         
      }
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
      start_up(){
        this.$ajax({
              type: 'HEAD',
              method: 'post',
              url: this.url+'/administrator/start_up/',
              withCredentials: true,
              crossDomain:true,
              changeOrigin: true,
              })
              .then((response) => {    
                if(response.status == 200){
                  this.$message.success('启动服务成功！');
                }
              })
              .catch((error) => {
                this.$message.error(error.response.data.message);
              })
      },
      check(formName){
        this.$refs[formName].validate((valid) => {
          if (valid) {
            let sent ={
              room_id:this.checkForm.roomId
            }
             this.$ajax({
              type: 'HEAD',
              method: 'post',
              url: this.url+'/administrator/check_room_state/',
              data : sent,
               withCredentials: true,
              crossDomain:true,
              changeOrigin: true,
              })
              .then((response) => {    
                if(response.status == 200){
                  this.isCheckIn = this.chechen[response.data.isCheckIn]
                  this.isOpen = this.open[response.data.isOpen]
                  this.isServing = this.serving[response.data.isServing]
                  this.cur_temp = response.data.current_temp
                  this.tar_temp = response.data.target_temp
                  this.fee_rate = response.data.fee_rate
                  this.fee = response.data.fee
                  if(response.data.wind == 'high'){
                    this.cur_wind = '强风'
                  }else if (response.data.wind == 'mid'){
                    this.cur_wind = '中风'
                  }else if(response.data.wind == 'low'){
                    this.cur_wind = '弱风'
                  }
                }
              })
              .catch((error) => {
                this.$message.error(error.response.data.message);
              })   
          }else{
            this.$message.error('请检查输入是否正确！');
              return false;
            }
        });
      },
      set_para(formName){
        
        this.$refs[formName].validate((valid) => {
          if (valid) {
             let sent = {
               model:this.form.model,
               temp_high_limit:this.form.maxt,
               temp_low_limit:this.form.mint,
               default_target_temp:this.form.target,
               fee_rate_h:this.form.fee_rate_h,
               fee_rate_m:this.form.fee_rate_m,
               fee_rate_l:this.form.fee_rate_l,
               num_rooms:this.form.num_rooms,
               num_serve:this.form.num_serve
             }
             this.$ajax({
              type: 'HEAD',
              method: 'post',
              url: this.url+'/administrator/set_para/',
              data : sent,
               withCredentials: true,
              crossDomain:true,
              changeOrigin: true,
              })
              .then((response) => {    
                if(response.status == 200){
                  this.$message.success('设置成功！请启动服务。');
                  this.disabled = false
                }
              })
              .catch((error) => {
                this.$message.error(error.response.data.message);
              })
          }else {
            this.$message.error('请检查输入是否正确！');
            return false;
          }
        });
      },
      changemint(){
        if(this.form.mint>=this.form.maxt){
          this.form.mint = this.form.maxt - 1
        }
      },
      changemaxt(){
        if(this.form.mint<=this.form.maxt){
          this.form.maxt = this.form.mint + 1
        }
      },
      to_home(){
        this.$router.push('/');
      },
      power_on(){
          this.$ajax({
              type: 'HEAD',
              method: 'post',
              url: this.url+'/administrator/power_on/',
              withCredentials: true,
              crossDomain:true,
              changeOrigin: true,
            })
            .then((response) => {    
              if(response.status == 200){
                this.isPoweron = '已开机'
              }
            })
            .catch((error) => {
               this.$message.error(error.response.data.message);
            })
      },
      power_off(){
        this.$ajax({
              type: 'HEAD',
              method: 'post',
              url: this.url+'/administrator/power_off/',
              withCredentials: true,
              crossDomain:true,
              changeOrigin: true,
            })
            .then((response) => {    
              if(response.status == 200){
                this.isPoweron = '已关机'
              }
            })
            .catch((error) => {
               this.$message.error(error.response.data.message);
            })
      }
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
  .room{
     border-radius: 15px;
    line-height: 30px;
    position: relative;
    left: 28%;
    width: 300px;
    top: 30px;
    padding-top: 10px;
    padding-right: 10px;
    padding-bottom: 20px;
    text-align:center;
    background:rgba(255, 255, 255, 0.7);
  }
.checkf{
   border-radius: 15px;
    line-height: 30px;
    position: relative;
    left: 28%;
    width: 300px;
    padding-top: 30px;
    padding-right: 10px;
    text-align:center;
    background:rgba(255, 255, 255, 0.7);
}
.line{
  height: 20px;
}
  .set_p{
    border-radius: 15px;
    line-height: 20px;
    position: relative;
    left: 28%;
    top:25px;
    width: 300px;
    padding: 15px;
    text-align:center;
    background:rgba(255, 255, 255, 0.7);
  }
  .power_on{
    border-radius: 15px;
    line-height: 30px;
    position: relative;
    left: 28%;
    width: 300px;
    padding: 15px;
    text-align:center;
    background:rgba(255, 255, 255, 0.7);
  }
  .text{
    font-size:15px;
    position: relative;
   
    
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
