<script setup>
import { onMounted, ref, watch } from 'vue';
import { getAPI, putAPI } from '@/httpreqs';

const props = defineProps(['items']);

const professionals = ref([]);

const selectMode = ref(false);
const selectedIDs = ref([]);
const selectAll = ref(false);

const message = ref("");


async function initialLoad() {
    const response = await getAPI({ url: "/api/professional" });
    professionals.value = response.data.professionals;
}


function onToggleSelect() {
    selectMode.value = !selectMode.value;
    selectAll.value = false;
    selectedIDs.value = [];
}


async function onApproveSelectedClick() {
    try {
        const response = await putAPI({ url: "/api/professional", data: { "approve_selected": true, "ids": selectedIDs.value } });
        if (response.data.edited) {
            selectMode.value = false;
            message.value = "Professsionals Approved Successfully";
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

async function onRejectSelectedClick() {
    try {
        const response = await putAPI({ url: "/api/professional", data: { "reject_selected": true, "ids": selectedIDs.value } });
        if (response.data.edited) {
            selectMode.value = false;
            message.value = "Professsionals Rejected Successfully";
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
    professionals.value = newItems;
})

watch(selectAll, async (newVal, oldVal) => {
    if (newVal) {
        selectedIDs.value = professionals.value.map((prof) => prof.id);
    } else {
        selectedIDs.value = [];
    }
});

onMounted(async function () {
    if (props.items.length) {
        professionals.value = props.items;
    } else {
        initialLoad();
    }
});

</script>
<template>
    <!-- Professional List Table -->
    <section class="card rounded-sm w-3/4 border-2 border-primary-content/25">
        <div class="card-body">
            <h2 class="text-xl font-semibold">PROFESSIONALS</h2>

            <div v-if="message" class="bg-warning font-semibold p-4 my-4 rounded-md border-2 border-warning-content/50">
                {{ message }}
            </div>

            <div v-show="selectMode" class="flex items-center justify-end gap-2">
                <button @click="onApproveSelectedClick" class="btn btn-sm btn-success">
                    👍 APPROVE SELECTED
                </button>
                <button @click="onRejectSelectedClick" class="btn btn-sm btn-error">
                    👎 REJECT SELECTED
                </button>
            </div>

            <table class="table table-sm">
                <thead>
                    <tr>
                        <th v-show="selectMode">
                            <input type="checkbox" v-model="selectAll">
                        </th>
                        <th>ID</th>
                        <th>NAME</th>
                        <th>SERVICE</th>
                        <th>RATING</th>
                        <th>STATUS</th>
                        <th>APPLIED</th>
                        <th>ACTIONS</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-if="professionals.length" v-for="prof in professionals" :key="prof.id">
                        <td v-show="selectMode">
                            <input type="checkbox" :value="prof.id" v-model="selectedIDs" />
                        </td>
                        <td>
                            <RouterLink :to="{ name: 'admin_professional_details', params: { id: prof.id } }">
                                <button class="btn btn-sm">{{ prof.id }}</button>
                            </RouterLink>
                        </td>
                        <td>{{ prof.user.fullname }}</td>
                        <td>{{ prof.service.name }}</td>
                        <td>{{ prof.avg_rating }}</td>
                        <td>
                            <span v-if="prof.approval === 'REJECTED'" class="badge badge-lg badge-error">{{
                                prof.approval }}</span>
                            <span v-else-if="prof.approval === 'PENDING'" class="badge badge-lg border-dashed">{{
                                prof.approval }}</span>
                            <span v-else class="badge badge-lg badge-success">{{ prof.approval }}</span>
                        </td>
                        <td>{{ prof.created }}</td>
                        <td>
                            <span class="flex gap-2">
                                <RouterLink :to="{ name: 'admin_professional_approve', params: { id: prof.id } }">
                                    <button class="btn btn-sm btn-success">👍 APPROVE</button>
                                </RouterLink>
                                <RouterLink :to="{ name: 'admin_professional_reject', params: { id: prof.id } }">
                                    <button class="btn btn-sm btn-error">👎 REJECT</button>
                                </RouterLink>
                            </span>
                        </td>
                    </tr>
                    <tr v-else>
                        <td colspan="7" class="text-center font-bold text-error-content text-lg">No Professionals Found
                        </td>
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