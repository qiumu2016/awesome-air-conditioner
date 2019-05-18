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
          <el-button class = "btn" @click = "to_login()"> 登录</el-button>
      </el-main>
     
  </el-container>

</template>

<style scoped>
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
    position: relative;
    float: left;
    width: 20%;
    height: 8%;
    left: 38%;
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
        username:'',
        imglist:[
          {id:1, src:require('../images/1.jpg')},
          {id:2, src:require('../images/2.jpg')},
        ]
      }
    },
    computed:{
    },
    mounted(){
      //console.log(this.$store.getters.isLogin)
    },
    methods:{
      to_login(){
        console.log(123)
				this.$router.push('/login');
			},
    }
 };
</script>
