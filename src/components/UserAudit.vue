<template>
  <el-table :data="tableData" style="width: 100%">
    <el-table-column fixed prop="request_time" label="申请时间" sortable/>
    <el-table-column prop="name" label="姓名" sortable/>
    <el-table-column prop="operation_type" label="权限" sortable></el-table-column>
    <el-table-column prop="phone" label="手机号" sortable/>
    <el-table-column prop="username" label="用户名" sortable/>
    <el-table-column prop="email" label="邮箱" sortable/>
    <el-table-column fixed="right" label="审核">
      <template #default="scope">
        <div style="display: flex; flex-direction: row; flex-wrap: nowrap">
          <el-button type="success" size="default" @click="accept_request(scope.row)">通过</el-button>
          <el-button type="danger" size="default" @click="reject_request(scope.row)">不通过</el-button>
        </div>
      </template>
    </el-table-column>
  </el-table>
</template>

<script lang="ts" setup>
import {onMounted, ref} from 'vue';
import axios from "axios";
import {ElNotification} from "element-plus";
function init_tableData() {
  axios.get('/admin/all_users_to_register').then((res) => {
    tableData.value = res.data;
  }).catch((err) => {
    console.log(err);
  });
}
onMounted(() => {
  init_tableData();
});
function accept_request(row) {
  console.log(row)
  // 需要username, email, phone, name
  axios.post('/admin/accept_register', {
    username: row.username,
    email: row.email,
    phone: row.phone,
    name: row.name,
  }).then((res) => {
    console.log(res.data)
    ElNotification({
      title: '提示信息',
      message: res.data['msg'],
      type: res.data.type,
      duration: 3000,
      showClose: true,
      position: 'top-left',
    });
    if (res.data.type === 'success') {
      init_tableData();
    }
  }).catch((err) => {
    console.log(err);
  });
}
function reject_request(row) {
  // 需要username, email, phone, name

  axios.post('/admin/reject_register', {
    username: row.username,
    email: row.email,
    phone: row.phone,
    name: row.name,
  }).then((res) => {
    ElNotification({
      title: '提示信息',
      message: res.data['msg'],
      type: res.data.type,
      duration: 3000,
      showClose: true,
      position: 'top-left',
    });
    if (res.data.type === 'warning') {
      init_tableData();
    }
  }).catch((err) => {
    console.log(err);
  });
}

const tableData = ref([
  {
    request_time: '',
    name: '',
    phone: '',
    username: '',
    email: '',
  },
])
</script>
