<script setup lang="js">
import { RouterLink } from 'vue-router';
import { ArrowRightBold, ArrowLeftBold } from '@element-plus/icons-vue';
import { reactive } from 'vue';

const form = reactive({
    interest: '',
    bidding: ''
});

const tableData = reactive([
    { role: '2016-05-02', interest: 'John', bidding: 'New York' },
    { role: '2016-05-04', interest: 'Tom', bidding: 'Washington' },
    { role: '2016-05-01', interest: 'Lily', bidding: 'Texas' },
    { role: '2016-05-03', interest: 'Rose', bidding: 'Florida' }
]);

</script>

<template>
    <div>
        <el-form style="padding: 10px" v-model="form">
            <el-form-item lable="interest">
                <el-select v-model="form.interest" placeholder="Select Interest" clearable>
                    <el-option lable="lable1" value="value1" />
                    <el-option lable="lable2" value="value2" />
                </el-select>
            </el-form-item>
            <el-form-item lable="bidding">
                <el-input v-model="form.bidding" placeholder="Enter Bidding" />
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="bid">Add</el-button>
            </el-form-item>
        </el-form>
    </div>
    <div>
        <el-table :data="tableData" style="width: 100%" :row-class-name="tableRowClassName">
            <el-table-column prop="role" label="Role" width="180" />
            <el-table-column prop="interest" label="Interest" width="180" />
            <el-table-column prop="bidding" label="Bidding" />
        </el-table>
    </div>
</template>

<style>
.demo-form-inline .el-input {
    --el-input-width: 220px;
}

.demo-form-inline .el-select {
    --el-select-width: 220px;
}

</style>