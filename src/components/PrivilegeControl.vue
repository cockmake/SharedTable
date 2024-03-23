<template>
  <div>
    <el-table :data="filterTableData" style="width: 100%">
      <el-table-column label="姓名" prop="name" sortable width="100" fixed/>
      <el-table-column label="用户名" prop="username" sortable width="150">
        <template #default="scope">
          <el-tag size="large" type="primary">{{ scope.row.username }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="日期" prop="rq" sortable width="80">
        <template #default="scope">
          <el-tag size="large" :type="judge_type(scope.row.rq)">{{ scope.row.rq }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="司机" prop="sj" sortable width="80">
        <template #default="scope">
          <el-tag size="large" :type="judge_type(scope.row.sj)">{{ scope.row.sj }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="车号" prop="ch" sortable width="80">
        <template #default="scope">
          <el-tag size="large" :type="judge_type(scope.row.ch)">{{ scope.row.ch }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="车型" prop="cx" sortable width="80">
        <template #default="scope">
          <el-tag size="large" :type="judge_type(scope.row.cx)">{{ scope.row.cx }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="签单" prop="qd" sortable width="80">
        <template #default="scope">
          <el-tag size="large" :type="judge_type(scope.row.qd)">{{ scope.row.qd }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="车属单位" prop="csdw" sortable width="110">
        <template #default="scope">
          <el-tag size="large" :type="judge_type(scope.row.csdw)">{{ scope.row.csdw }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="用车单位" prop="ycdw" sortable width="110">
        <template #default="scope">
          <el-tag size="large" :type="judge_type(scope.row.ycdw)">{{ scope.row.ycdw }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="用车时间" prop="ycsj" sortable width="110">
        <template #default="scope">
          <el-tag size="large" :type="judge_type(scope.row.ycsj)">{{ scope.row.ycsj }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="行程" prop="xc" sortable width="80">
        <template #default="scope">
          <el-tag size="large" :type="judge_type(scope.row.xc)">{{ scope.row.xc }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="金额" prop="je" sortable width="80">
        <template #default="scope">
          <el-tag size="large" :type="judge_type(scope.row.je)">{{ scope.row.je }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="收" prop="shou" sortable width="80">
        <template #default="scope">
          <el-tag size="large" :type="judge_type(scope.row.shou)">{{ scope.row.shou }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="票" prop="piao" sortable width="80">
        <template #default="scope">
          <el-tag size="large" :type="judge_type(scope.row.piao)">{{ scope.row.piao }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="应付" prop="yf" sortable width="80">
        <template #default="scope">
          <el-tag size="large" :type="judge_type(scope.row.yf)">{{ scope.row.yf }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="付" prop="fu" sortable width="80">
        <template #default="scope">
          <el-tag size="large" :type="judge_type(scope.row.fu)">{{ scope.row.fu }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="结余" prop="jy" sortable width="80">
        <template #default="scope">
          <el-tag size="large" :type="judge_type(scope.row.jy)">{{ scope.row.jy }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="备注" prop="bz" sortable width="80">
        <template #default="scope">
          <el-tag size="large" :type="judge_type(scope.row.bz)">{{ scope.row.bz }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="可添加" prop="can_add" sortable width="90">
        <template #default="scope">
          <el-tag size="large" :type="judge_type(scope.row.can_add)">{{ scope.row.can_add }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="可删除" prop="can_delete" sortable width="90">
        <template #default="scope">
          <el-tag size="large" :type="judge_type(scope.row.can_delete)">{{ scope.row.can_delete }}</el-tag>
        </template>
      </el-table-column>

      <el-table-column fixed width="130">
        <template #header>
          <el-input v-model="search" placeholder="姓名搜索"/>
        </template>
        <template #default="scope">
          <div style="display: flex; flex-direction: row; flex-wrap: nowrap">
            <el-button
                type="primary"
                @click="handleEdit(scope.$index, scope.row)">修改权限
            </el-button>
<!--            <el-button-->
<!--                type="danger"-->
<!--                @click="handleDelete(scope.$index, scope.row)">删除用户-->
<!--            </el-button>-->
          </div>

        </template>
      </el-table-column>
    </el-table>
    <el-dialog v-model="dialogVisible" title="权限编辑" width="60%" draggable destroy-on-close style="border-radius: 1%">
      <div style="width: 100%; height: 100%; display: flex; justify-content: center; align-items: center">
        <el-form :model="current_user" label-width="auto" style="width: 80%" label-position="right">
          <el-form-item label="姓名">
            <el-input v-model="current_user.name" disabled/>
          </el-form-item>
          <el-form-item label="用户名">
            <el-input v-model="current_user.username" disabled/>
          </el-form-item>
          <el-form-item label="可操作权限">
            <div>
              <el-checkbox border size="large" v-model="current_user.rq">日期</el-checkbox>
              <el-checkbox border size="large" v-model="current_user.sj">司机</el-checkbox>
              <el-checkbox border size="large" v-model="current_user.ch">车号</el-checkbox>
              <el-checkbox border size="large" v-model="current_user.cx">车型</el-checkbox>
              <el-checkbox border size="large" v-model="current_user.qd">签单</el-checkbox>
              <el-checkbox border size="large" v-model="current_user.csdw">车属单位</el-checkbox>
              <el-checkbox border size="large" v-model="current_user.ycdw">用车单位</el-checkbox>
              <el-checkbox border size="large" v-model="current_user.ycsj">用车时间</el-checkbox>
              <el-checkbox border size="large" v-model="current_user.xc">行程</el-checkbox>
              <el-checkbox border size="large" v-model="current_user.je">金额</el-checkbox>
              <el-checkbox border size="large" v-model="current_user.shou">收</el-checkbox>
              <el-checkbox border size="large" v-model="current_user.piao">票</el-checkbox>
              <el-checkbox border size="large" v-model="current_user.yf">应付</el-checkbox>
              <el-checkbox border size="large" v-model="current_user.fu">付</el-checkbox>
              <el-checkbox border size="large" v-model="current_user.jy">结余</el-checkbox>
              <el-checkbox border size="large" v-model="current_user.bz">备注</el-checkbox>
              <el-checkbox border size="large" v-model="current_user.can_add">可添加</el-checkbox>
              <el-checkbox border size="large" v-model="current_user.can_delete">可删除</el-checkbox>

            </div>
          </el-form-item>
        </el-form>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="editConfirm">
            确认
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>

</template>

<script lang="ts" setup>
import {computed, onMounted, ref} from 'vue'
import axios from "axios";
import {ElNotification} from "element-plus";
function judge_type(value: string) {
  return value === '√' ? 'success' : 'danger';
}
const dialogVisible = ref(false)
function init_users_privilege() {
  axios.get('/admin/get_users_privilege').then((res) => {
    tableData.value = res.data;
  }).catch((err) => {
    console.log(err);
  });

}

onMounted(() => {
  init_users_privilege();
})

interface User {
  username: string
  name: string
  rq: string
  sj: string
  ch: string
  cx: string
  qd: string
  csdw: string
  ycdw: string
  ycsj: string
  xc: string
  je: string
  shou: string
  piao: string
  yf: string
  fu: string
  jy: string
  bz: string
  can_add: string
  can_delete: string
}

const search = ref('')
const filterTableData = computed(() =>
    tableData.value.filter(
        (data) =>
            !search.value ||
            data.name.toLowerCase().includes(search.value.toLowerCase())
    )
)
const current_user = ref({} as User)
const editConfirm = () => {
  let data = {
    username: current_user.value.username,
    name: current_user.value.name,
    new_privilege: {
      rq: current_user.value.rq ? '√' : '×',
      sj: current_user.value.sj ? '√' : '×',
      ch: current_user.value.ch ? '√' : '×',
      cx: current_user.value.cx ? '√' : '×',
      qd: current_user.value.qd ? '√' : '×',
      csdw: current_user.value.csdw ? '√' : '×',
      ycdw: current_user.value.ycdw ? '√' : '×',
      ycsj: current_user.value.ycsj ? '√' : '×',
      xc: current_user.value.xc ? '√' : '×',
      je: current_user.value.je ? '√' : '×',
      shou: current_user.value.shou ? '√' : '×',
      piao: current_user.value.piao ? '√' : '×',
      yf: current_user.value.yf ? '√' : '×',
      fu: current_user.value.fu ? '√' : '×',
      jy: current_user.value.jy ? '√' : '×',
      bz: current_user.value.bz ? '√' : '×',
      can_add: current_user.value.can_add ? '√' : '×',
      can_delete: current_user.value.can_delete ? '√' : '×',
    }
  }
  axios.post('/admin/update_user_privilege', data).then((res) => {
    ElNotification({
      title: '提示信息',
      message: res.data['msg'],
      type: res.data.type,
      duration: 3000,
      showClose: true,
      position: 'top-right',
    });
    if (res.data.type === 'success') {
      // 本地修改到tableData
      // 遍历tableData根据data进行修改
      for (let i = 0; i < tableData.value.length; i++) {
        if (tableData.value[i].username === data.username && tableData.value[i].name === data.name) {
          for (let key in data.new_privilege) {
            tableData.value[i][key] = data.new_privilege[key];
          }
          break;
        }
      }
      dialogVisible.value = false
    }
  }).catch((err) => {
    console.log(err);
  });
}
const handleEdit = (index: number, row: User) => {
  dialogVisible.value = true
  // 复制一份数据不要直接指向
  current_user.value = {...row}
  for (let key in current_user.value) {
    if (key === 'username' || key === 'name') continue;
    current_user.value[key] = current_user.value[key] === '√';
  }
}
// const handleDelete = (index: number, row: User) => {
//   console.log(index, row)
// }

const tableData = ref([] as User[])
</script>


<style scoped>

</style>