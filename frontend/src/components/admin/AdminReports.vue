<script setup>
import { onMounted, ref } from 'vue';
import { getAPI, deleteAPI, postAPI } from '@/httpreqs';

const reports = ref([]);

const message = ref("");

async function initialLoad() {
    const response = await getAPI({ url: "/api/report" });
    reports.value = response.data.reports;
    if (!reports.value.length) {
        message.value = 'No reports found; Click generate to create one';
    }
}

async function onGenerateClick() {
    const response = await postAPI({ url: "/api/report", data: {} });
    if (response.data.added) {
        message.value = 'Report Successfully Generated';
        setTimeout(() => {
            initialLoad();
            message.value = '';
        }, 1000)
    }
}

async function onDeleteClick(reportName) {
    const response = await deleteAPI({ url: "/api/report", params: { 'name': reportName } });
    if (response.data.deleted) {
        message.value = 'Report Successfully Deleted';
        setTimeout(() => {
            initialLoad();
            message.value = '';
        }, 1000)
    }
}

onMounted(async function () {
    initialLoad();
})

</script>

<template>
    <section class="card rounded-sm w-3/4 border-2 border-primary-content/25">
        <div class="card-body">
            <h2 class="text-xl font-semibold">REPORTS</h2>

            <div v-if="message" class="bg-warning font-semibold p-4 my-4 rounded-md border-2 border-warning-content/50">
                {{ message }}
            </div>

            <table v-if="reports.length" class="table table-sm">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>REPORT</th>
                        <th>ACTIONS</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="report in reports" :key="report.id">
                        <td>{{ report.id }}</td>
                        <td>{{ report.name }}</td>
                        <td>
                            <span class="flex gap-2">
                                <a :href="report.url" download>
                                    <button class="btn btn-sm btn-warning">DOWNLOAD</button>
                                </a>
                                <button @click="onDeleteClick(report.name)" class="btn btn-sm btn-error">
                                    DELETE
                                </button>
                            </span>
                        </td>
                    </tr>
                </tbody>
            </table>

            <div class="flex items-center justify-end gap-2">
                <button @click="onGenerateClick" class="btn btn-sm btn-success">
                    GENERATE
                </button>
            </div>
        </div>
    </section>
</template>