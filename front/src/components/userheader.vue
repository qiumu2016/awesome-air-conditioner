<template>
		  <el-row :gutter="20">
        <el-menu 
          :default-active="'0'" 
          class="el-menu-demo" 
          mode="horizontal" 
          active-text-color="#000000"
        >
          <el-col :span="10" :offset="1"><pre></pre></el-col>

          <el-menu-item index="0" @click="to_home">
            <span class="iconfont">&#xe61e;</span>
          ACC空调管理系统
          </el-menu-item>

						<el-col :span="5" :offset="1"><pre></pre></el-col>

					 <el-menu-item index="1" @click="log_out">
            <span class="iconfont">&#xe66a;</span>
          登出
          </el-menu-item>
       </el-menu>
      </el-row>
</template>

<script>
  export default {
		name:'header',
    data() {
      return {
				
      }
		},
    methods:{
			//handleSelect(key, keyPath)
      to_home(){
        this.$router.push('/')
			},
			to_login(){
				this.$router.push('/login')
			},
			log_out(){
          this.$ajax({
          type: 'HEAD',
          method: 'DELETE',
          url: '/api/session',
          withCredentials: true, 
          crossDomain: true
        })
        this.$router.push('/login')
      },
    }
  };
</script>

