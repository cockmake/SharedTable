<script setup lang="ts">
import { ref } from 'vue'
import UserAudit from './components/UserAudit.vue'
import PrivilegeControl from './components/PrivilegeControl.vue'
const show_user_audit =  ref(false)
</script>

<template>
  <div style="height: 100%; width: 100%">
    <div style="display: flex; flex-direction: row; flex-wrap: nowrap;  justify-content: center; align-items: center">
      <el-button type="warning" size="large" @click="show_user_audit = true">用户审核</el-button>
      <el-button type="primary" size="large" @click="show_user_audit = false">权限控制</el-button>
    </div>
    <div>
      <UserAudit v-if="show_user_audit"/>
      <PrivilegeControl v-else/>
    </div>
  </div>
</template>

<style scoped>

</style>
