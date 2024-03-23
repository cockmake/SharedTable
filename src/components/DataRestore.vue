<template>
  <el-table :data="tableData" style="width: 100%">
    <el-table-column fixed prop="record_id" label="序号" width="80" sortable/>
    <el-table-column prop="rq" label="日期" width="130" sortable/>
    <el-table-column prop="sj" label="司机" width="100" sortable/>
    <el-table-column prop="ch" label="车号" width="100" sortable/>
    <el-table-column prop="cx" label="车型" width="100" sortable/>
    <el-table-column prop="qd" label="签单" width="100" sortable/>
    <el-table-column prop="csdw" label="车属单位" width="110" sortable/>
    <el-table-column prop="ycdw" label="用车单位" width="110" sortable/>
    <el-table-column prop="ycsj" label="用车时间" width="200" sortable/>
    <el-table-column prop="xc" label="行程" width="350" sortable/>
    <el-table-column prop="fu" label="付" width="70" sortable/>
    <el-table-column prop="je" label="金额" width="100" sortable/>
    <el-table-column prop="jy" label="结余" width="100" sortable/>
    <el-table-column prop="yf" label="应付" width="100" sortable/>
    <el-table-column prop="piao" label="票" width="70" sortable/>
    <el-table-column prop="shou" label="收" width="70" sortable/>
    <el-table-column prop="bz" label="备注" width="150" sortable/>

    <el-table-column fixed="right" label="操作" width="120">
      <template #default="scope">
        <el-button type="success" @click="handleRestore(scope.row)">恢复</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script lang="ts" setup>
import {onMounted, ref} from "vue";
import axios from "axios";
import {ElNotification} from "element-plus";

function get_all_drop_data() {
  axios.get('/admin/all_drop_data').then((res) => {
    console.log(res.data)
    tableData.value = res.data
  }).catch((err) => {
    console.log(err)
  })
}
function handleRestore(row) {
  // 需要提供record_id
  // 额外提供日期，司机，车号做判定
  axios.post('/admin/restore_drop_data', {
    record_id: row.record_id,
    rq: row.rq,
    sj: row.sj,
    ch: row.ch,
  }).then((res) => {
    console.log(res.data)
    ElNotification({
      title: '提示信息',
      message: res.data['msg'],
      type: res.data.type,
      duration: 3000,
      showClose: true,
      position: 'top-right',
    });
    if (res.data.type === 'success') {
      // 在本地删除这一行
      tableData.value = tableData.value.filter((item) => item.record_id !== row.record_id)
    }
  }).catch((err) => {
    console.log(err)
  })


}

onMounted(() => {
  get_all_drop_data()
})


const tableData = ref([])
</script>
