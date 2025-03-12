<script setup>
import { onMounted, ref, watch } from 'vue';
import { getAPI, putAPI } from '@/httpreqs';

const props = defineProps(['items']);

const customers = ref([]);

const selectMode = ref(false);
const selectedIDs = ref([]);
const selectAll = ref(false);

const message = ref("");


async function initialLoad() {
    const response = await getAPI({ url: "/api/customer" });
    customers.value = response.data.customers;
}


function onToggleSelect() {
    selectMode.value = !selectMode.value;
    selectAll.value = false;
    selectedIDs.value = [];
}


async function onActivateSelectedClick() {
    try {
        const response = await putAPI({ url: "/api/customer", data: { "activate_selected": true, "ids": selectedIDs.value } });
        if (response.data.edited) {
            selectMode.value = false;
            message.value = "Customers Activated Successfully";
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

async function onBlockSelectedClick() {
    try {
        const response = await putAPI({ url: "/api/customer", data: { "block_selected": true, "ids": selectedIDs.value } });
        if (response.data.edited) {
            selectMode.value = false;
            message.value = "Customers Blocked Successfully";
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
    customers.value = newItems;
});

watch(selectAll, async (newVal, oldVal) => {
    if (newVal) {
        selectedIDs.value = customers.value.map((prof) => prof.id);
    } else {
        selectedIDs.value = [];
    }
});


onMounted(async function () {
    if (props.items.length) {
        customers.value = props.items;
    } else {
        initialLoad();
    }
})

</script>
<template>
    <section class="card rounded-sm w-3/4 border-2 border-primary-content/25">
        <div class="card-body">
            <h2 class="text-xl font-semibold">CUSTOMERS</h2>
            <div v-if="message" class="bg-warning font-semibold p-4 my-4 rounded-md border-2 border-warning-content/50">
                {{ message }}
            </div>

            <div v-show="selectMode" class="flex items-center justify-end gap-2">
                <button @click="onActivateSelectedClick" class="btn btn-sm btn-success">
                    ✅ ACTIVATE SELECTED
                </button>
                <button @click="onBlockSelectedClick" class="btn btn-sm btn-error">
                    ❌ BLOCK SELECTED
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
                        <th>EMAIL</th>
                        <th>CONTACT</th>
                        <th>STATUS</th>
                        <th>JOINED</th>
                        <th>ACTIONS</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-if="customers.length" v-for="customer in customers">
                        <td v-show="selectMode">
                            <input type="checkbox" :value="customer.id" v-model="selectedIDs" />
                        </td>
                        <td>
                            <RouterLink :to="{ name: 'admin_customer_details', params: { id: customer.id } }"
                                class="btn btn-sm">{{ customer.id }}</RouterLink>
                        </td>
                        <td>{{ customer.user.fullname }}</td>
                        <td>{{ customer.user.email }}</td>
                        <td>{{ customer.contact }}</td>
                        <td>
                            <span v-if="customer.status === 'ACTIVE'" class="badge badge-lg badge-success">{{
                                customer.status }}</span>
                            <span v-else class="badge badge-lg badge-error">{{ customer.status }}</span>
                        </td>
                        <td>{{ customer.created }}</td>
                        <td>
                            <span class="flex gap-2">
                                <RouterLink :to="{ name: 'admin_customer_activate', params: { id: customer.id } }">
                                    <button class="btn btn-sm btn-success">✅ ACTIVATE</button>
                                </RouterLink>
                                <RouterLink :to="{ name: 'admin_customer_block', params: { id: customer.id } }">
                                    <button class="btn btn-sm btn-error">❌ BLOCK</button>
                                </RouterLink>
                            </span>
                        </td>
                    </tr>
                    <tr v-else>
                        <td colspan="7" class="text-center font-bold text-error-content text-lg">No Customers Found</td>
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