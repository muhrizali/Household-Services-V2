<script setup>
import { onMounted, ref, watch } from 'vue';
import { deleteAPI, getAPI } from '@/httpreqs';

const services = ref([]);

const selectMode = ref(false);
const selectedIDs = ref([]);
const selectAll = ref(false);

const message = ref("");

async function onInitialLoad() {
    const response = await getAPI({ url: "/api/service", params: { all: true } });
    services.value = response.data.services;
}


function onToggleSelect() {
    selectMode.value = !selectMode.value;
    selectedIDs.value = [];
}

watch(selectAll, async (newVal, oldVal) => {
    if (newVal) {
        selectedIDs.value = services.value.map((service) => service.id);
    } else {
        selectedIDs.value = [];
    }
});

async function onDeleteSelectedClick() {
    try {
        const response = await deleteAPI({ url: "/api/service", params: { ids: selectedIDs.value } });
        if (response.data.deleted) {
            selectMode.value = false;
            message.value = "Services Deleted Successfully";
            setTimeout(() => {
                message.value = "";
                selectedIDs.value = [];
                onInitialLoad();
                
            }, 2000);
        }
    } catch {
        selectMode.value = false;
        message.value = "Some Error Occured";
        setTimeout(() => {
            message.value = "";
            selectedIDs.value = [];
        }, 2000);
    }
}

onMounted(onInitialLoad);

</script>

<template>
    <section class="card rounded-sm w-3/4 border-2 border-primary-content/25">
        <div class="card-body">
            <h2 class="text-xl font-semibold">SERVICES</h2>

            <div v-if="message" class="bg-warning font-semibold p-4 my-4 rounded-md border-2 border-warning-content/50">
                {{ message }}
            </div>

            <div v-show="selectMode" class="flex items-center justify-end gap-2">
                <button @click="onDeleteSelectedClick" class="btn btn-sm btn-error">
                    🗑️ DELETED SELECTED
                </button>
            </div>

            <table class="table table-sm">
                <thead>
                    <tr>
                        <th v-show="selectMode">
                            <input type="checkbox" v-model="selectAll">
                        </th>
                        <th>ID</th>
                        <th>SERVICE</th>
                        <th>PRICE</th>
                        <th>CREATED</th>
                        <th>ACTIONS</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-if="services.length" v-for="service in services" :key="service.id">
                        <td v-show="selectMode">
                            <input type="checkbox" :value="service.id" v-model="selectedIDs">
                        </td>
                        <td>
                            <RouterLink :to="{ name: 'admin_service_details', params: { id: service.id } }">
                                <button class="btn btn-sm">{{ service.id }}</button>
                            </RouterLink>
                        </td>
                        <td>{{ service.name }}</td>
                        <td>{{ service.price }}</td>
                        <td>{{ service.created }}</td>
                        <td>
                            <span class="flex gap-2">
                                <RouterLink :to="{ name: 'admin_service_edit', params: { id: service.id } }">
                                    <button class="btn btn-sm btn-warning">✏️ EDIT</button>
                                </RouterLink>
                                <RouterLink :to="{ name: 'admin_service_delete', params: { id: service.id } }">
                                    <button class="btn btn-sm btn-error">🗑️ DELETE</button>
                                </RouterLink>
                            </span>
                        </td>
                    </tr>
                    <tr v-else>
                        <td colspan="5" class="text-center font-bold text-error-content text-lg">No Services Found</td>
                    </tr>
                </tbody>
            </table>

            <!-- Add Service button -->
            <div class="flex items-center justify-end gap-2">
                <button @click="onToggleSelect" class="btn btn-sm btn-info">
                    {{ selectMode ? "❌ UNSELECT" : "✅ SELECT" }}
                </button>
                <RouterLink :to="{ name: 'admin_service_create' }">
                    <button class="btn btn-sm btn-success">
                        <!-- + New Service -->
                        ➕ NEW SERVICE
                    </button>
                </RouterLink>
            </div>
        </div>
    </section>
</template>