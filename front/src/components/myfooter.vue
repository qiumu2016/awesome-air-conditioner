<template>
	<!-- <el-footer> -->
		<el-row type="flex" class="row-bg" justify="space-around">
			<el-col :span="6">

				<el-popover
				  class="left"
					placement="top"
					width="202"
					trigger="hover">
					<span style="position: relative;right:-15%">前端工程：&nbsp;&nbsp;</span><br/>
					<span style="position: relative;right:-15%">后端工程：</span><br/>
					<el-button type="text" slot="reference" style="font-size:17px;color:#FFF">关于我们</el-button>
				</el-popover>

			</el-col>
			<el-col :span="6">

				<el-popover
				  class="left"
					placement="top"
					width="240"
					trigger="hover">
					<span style="position: relative;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;本项目前端工程基于Vue框架开发，后端工程基于Django框架开发，本小组成员保留对一切bug的解释权。</span><br/>
					<el-button type="text" slot="reference" style="font-size:17px;color:#FFF">关于项目</el-button>
				</el-popover>

			</el-col>
		</el-row>
	<!-- </el-footer> -->
</template>

<style>

</style>

<script>
  export default {
    name: 'footer',
    data() {
      return {
        
      }
    },
    methods:{

    }
  };
</script>
