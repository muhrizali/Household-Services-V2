<script setup>
import { onMounted, ref, watch } from 'vue';
import { deleteAPI, getAPI } from '@/httpreqs';

const props = defineProps(['items']);

const requests = ref([]);

const selectMode = ref(false);
const selectedIDs = ref([]);
const selectAll = ref(false);

const message = ref("");


async function initialLoad () {
    const response = await getAPI({ url: "/api/request" });
    requests.value = response.data.requests;
}


function onToggleSelect() {
    selectMode.value = !selectMode.value;
    selectAll.value = false;
    selectedIDs.value = [];
}

async function onDeleteSelectedClick() {
    try {
        const response = await deleteAPI({ url: "/api/request", params: { "ids": selectedIDs.value } });
        if (response.data.deleted) {
            selectMode.value = false;
            message.value = "Service Requests Deleted Successfully";
        }
    } catch {
        selectMode.value = false;
        message.value = "Some Error Occured";
    }
    setTimeout(() => {
        message.value = "";
        selectedIDs.value = [];
        initialLoad();
    }, 1000);
}

watch(() => props.items, (newItems, oldItems) => {
    requests.value = newItems;
})

watch(selectAll, async (newVal, oldVal) => {
    if (newVal) {
        selectedIDs.value = requests.value.map((prof) => prof.id);
    } else {
        selectedIDs.value = [];
    }
});

onMounted(async function () {
    if (props.items.length) {
        requests.value = props.items;
    } else {
        initialLoad();
    }
})

</script>
<template>
    <!-- Service Requests List Table -->
    <section class="card rounded-sm w-3/4 border-2 border-primary-content/25">
        <div class="card-body">
            <h2 class="text-xl font-semibold">SERVICE REQUESTS</h2>

            <div v-if="message" class="bg-warning font-semibold p-4 my-4 rounded-md border-2 border-warning-content/50">
                {{ message }}
            </div>

            <div v-show="selectMode" class="flex items-center justify-end gap-2">
                <button @click="onDeleteSelectedClick" class="btn btn-sm btn-error">
                    🗑️ DELETE SELECTED
                </button>
            </div>

            <table class="table table-sm">
                <thead>
                    <tr>
                        <th v-show="selectMode">
                            <input type="checkbox" v-model="selectAll">
                        </th>
                        <th>ID</th>
                        <th>CUSTOMER</th>
                        <th>SERVICE</th>
                        <th>PROFESSIONAL</th>
                        <th>REQUESTED</th>
                        <th>STATUS</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-if="requests.length" v-for="request in requests">
                        <td v-show="selectMode">
                            <input type="checkbox" :value="request.id" v-model="selectedIDs" />
                        </td>
                        <td>
                            <RouterLink :to="{ name: 'admin_request_details', params: { id: request.id } }">
                                <button class="btn btn-sm">{{ request.id }}</button>
                            </RouterLink>
                        </td>
                        <td>{{ request.customer.user.fullname }}</td>
                        <td>{{ request.service.name }}</td>
                        <td>
                            <span v-if="request.status === 'REQUESTED'">NOT ASSIGNED</span>
                            <span v-else>{{ request.professional.user.fullname }}</span>
                        </td>
                        <td>{{ request.created }}</td>
                        <td>
                            <span v-if="request.status === 'REQUESTED'"
                                class="badge badge-lg badge-error">REQUESTED</span>
                            <span v-else-if="request.status === 'ASSIGNED'"
                                class="badge badge-lg badge-warning">ASSIGNED</span>
                            <span v-else class="badge badge-lg badge-success">CLOSED</span>
                        </td>
                        <td>
                            <span class="flex gap-2">
                                <RouterLink :to="{ name: 'admin_request_edit', params: { id: request.id } }">
                                    <button class="btn btn-sm btn-warning">✏️ EDIT</button>
                                </RouterLink>
                                <RouterLink :to="{ name: 'admin_request_delete', params: { id: request.id } }">
                                    <button class="btn btn-sm btn-error">🗑️ DELETE</button>
                                </RouterLink>
                            </span>
                        </td>
                    </tr>
                    <tr v-else>
                        <td colspan="6" class="text-center font-bold text-error-content text-lg">No Requests Found</td>
                    </tr>
                </tbody>
            </table>

            <div class="flex items-center justify-end gap-2">
                <button @click="onToggleSelect" class="btn btn-sm btn-info">
                    {{ selectMode ? "❌ UNSELECT" : "✅ SELECT" }}
                </button>
            </div>
        </div>
    </section>
</template>