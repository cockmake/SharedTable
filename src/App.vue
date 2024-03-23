<script setup lang="ts">
import { ref } from 'vue'
import UserAudit from './components/UserAudit.vue'
import PrivilegeControl from './components/PrivilegeControl.vue'
import DataRestore from './components/DataRestore.vue'
const page_control = ref([false, true, false])

function change_page(index: number) {
  for (let i = 0; i < page_control.value.length; i++) {
    page_control.value[i] = i === index
  }
}
</script>

<template>
  <div style="height: 100%; width: 100%">
    <div style="display: flex; flex-direction: row; flex-wrap: nowrap;  justify-content: center; align-items: center">
      <el-button type="warning" size="large" @click="change_page(0)">用户审核</el-button>
      <el-button type="primary" size="large" @click="change_page(1)">权限控制</el-button>
      <el-button type="success" size="large" @click="change_page(2)">数据恢复</el-button>
    </div>
    <div>
      <UserAudit v-if="page_control[0]"/>
      <PrivilegeControl v-if="page_control[1]"/>
      <DataRestore v-if="page_control[2]"/>
    </div>
  </div>
</template>

<style scoped>

</style>
