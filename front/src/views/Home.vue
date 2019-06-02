<template>
  <el-container>
    <el-header>
        <el-row :gutter="20">
        <el-menu 
          :default-active="'0'" 
          class="el-menu-demo" 
          mode="horizontal" 
          active-text-color="#000000"
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
          <el-carousel :interval="4000" height="580px" style="z-index:1">
            <el-carousel-item v-for="item in imglist" :key="item">
              <div>
                <img :src = "item.src">
              </div>
            </el-carousel-item>
          </el-carousel>
           <el-card class="card" shadow="always">
              <div slot="header" class="clearfix">
                <span>参数设置</span>
              </div>
               <el-form ref="form" :model="form" label-width="130px">
                <el-form-item prop="url" :rules="[{ required: true, message: '请输入主机地址', trigger: 'blur' },]" label = "主机地址：">
                   <el-input placeholder="请输入地址" v-model="form.url">
                      <template slot="prepend">http://</template>
                    </el-input>
                </el-form-item>
                <el-form-item label = "房间号码：" prop="roomId" >
                   <el-input placeholder="非从机设置可不输入" v-model.number="form.roomId">
                    </el-input>
                </el-form-item>
                 <el-button  @click="set_para('form')" weight='50px' style="background-color:orange;color:white;width:100px">设置参数</el-button>
               </el-form>
            </el-card>
          <el-row :gutter="20">
            <el-col :span="6"><el-button :disabled='disable||roomable' class = "btn"  type="primary" @click = "to_costumer()"> 客房</el-button></el-col>
            <el-col :span="6"><el-button :disabled='disable' class = "btn"  type="success" @click = "to_desk()"> 前台</el-button></el-col>
            <el-col :span="6"><el-button :disabled='disable' class = "btn"  type="warning" @click = "to_manager()"> 经理</el-button></el-col>
            <el-col :span="6"><el-button :disabled='disable' class = "btn"  type="danger" @click = "to_administrator()"> 管理员</el-button></el-col>
          </el-row>
          
      </el-main>
     
  </el-container>

</template>

<style scoped>
  .card{
    position: absolute;
    top:50%;
    left: 30%;
    z-index: 20;
    height: 220px;
    width: 600px;
  }
  .body {
    min-height: 100%;
    margin: 0;
    padding: 0;
    position: relative;
   
  }
  .el-main {
    color: #333;
    background-size: 100% 100%;
    width: 100%;
    min-height: 100%;
    top: 60px;
    bottom: 20px;
    left: -3px;
    position: fixed;
  }
.btn{
    width: 50%;
    height: 8%;
    cursor: pointer;
    font-size: 20px;
}
 
</style>

<script>

  export default {
    name:'homepage',
    components: { 
  
    },
    data() {
      return {
        disable:true,
        roomable:true,
        form:{
          url:'',
          roomId:'',
        },
        username:'',
        imglist:[
          {id:1, src:require('../images/1.jpg')},
          {id:2, src:require('../images/2.jpg')},
        ]
      }
    },
    computed:{
    },
    created(){
      this.init()
    },
    mounted(){
      //console.log(this.$store.getters.isLogin)
    },
    methods:{
      init(){
        if(sessionStorage.getItem("url") !='null'){
          this.form.url = sessionStorage.getItem("url")
        }
      },
      set_para(formName){
         this.$refs[formName].validate((valid) => {
          if (valid) {
            sessionStorage.setItem("url",'http://'+this.form.url)
            sessionStorage.setItem("roomId",this.form.roomId)
            this.disable = false;
            if(this.form.roomId != ''){
              this.roomable = false
            }
          }else {
            this.$message.error('请检查输入是否正确！');
            return false;
          }
        });
      },
      to_costumer(){
				this.$router.push('/costumer');
      },
      to_desk(){
        this.$router.push('/desk');
      },
      to_manager(){
        this.$router.push('/manager');
      },
      to_administrator(){
         this.$router.push('/administrator');
      },
    }
 };
</script>
