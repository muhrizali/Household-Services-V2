<script setup>
import { useRoute } from 'vue-router';
import { onMounted, ref } from 'vue';
import { getAPI, putAPI } from '@/httpreqs';
const route = useRoute();
const serviceID = route.params.id;

const serviceFound = ref(false);
const service = ref({});

const name = ref("");
const description = ref("");
const price = ref(0);
const timereq = ref(0);

const message = ref("");

function servieEditData() {
    return {
        "id": serviceID,
        "name": name.value,
        "description": description.value,
        "price": price.value,
        "timereq": timereq.value
    };
}

async function onEditClick() {
    try {
        const response = await putAPI({ url: "/api/service", data: servieEditData() });
        if (response.data.edited) {
            message.value = "Service Successfully Updated";
        } else {
            message.value = "Service Could Not be Updated";
        }
        setTimeout(function () {
            message.value = "";
        }, 2000)
    } catch {
        message.value = "Error Occured while Updating Service";
    }
}

onMounted(async function () {
    try {
        const response = await getAPI({ url: "/api/service", params: { "id": serviceID } });
        if (response.data.found) {
            serviceFound.value = true;
            service.value = response.data.service;
            name.value = service.value.name;
            description.value = service.value.description;
            price.value = service.value.price;
            timereq.value = service.value.timereq;
        } else {
            serviceFound.value = false;
        }
    } catch (error) {
        message.value = "Something Went Wrong";
    }
})

</script>
<template>
    <div class="flex items-center justify-center w-full h-fit m-8">
        <div class="card card-bordered border-2 border-primary-content/25 w-2/3">
            <div class="card-body">
                <h2 class="card-title text-lg">EDIT SERVICE</h2>

                <div v-if="message" class="bg-warning font-semibold p-4 my-4 rounded-md border-2 border-warning-content/50">
                    {{ message }}
                </div>

                <div v-if="serviceFound">
                    <form class="form-control">
                        <table class="table table-sm">
                            <tbody>
                                <tr>
                                    <td>
                                        <label for="name">NAME:</label>
                                    </td>
                                    <td>
                                        <input id="name" type="text" class="input w-full input-bordered border-2"
                                            v-model="name">
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <label for="description">DESCRIPTION:</label>
                                    </td>
                                    <td>
                                        <textarea name="description" id="description"
                                            class="textarea w-full textarea-bordered border-2"
                                            rows="4">{{ description }}</textarea>
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <label for="price">PRICE:</label>
                                    </td>
                                    <td>
                                        <input id="price" type="text" class="input w-full input-bordered border-2"
                                            v-model="price">
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <label for="timereq">TIME REQUIRED (in hours):</label>
                                    </td>
                                    <td>
                                        <input id="timereq" type="number" class="input w-full input-bordered border-2"
                                            v-model="timereq">
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <div class="flex items-center justify-center mt-4">
                            <button @click.prevent="onEditClick" class="btn btn-block btn-lg btn-warning">EDIT</button>
                        </div>
                    </form>
                </div>
                <div v-else>
                    <p class="text-center text-lg font-bold">Requested Service Not Found</p>
                </div>

                <p class="text-center pt-2">
                    Go back to <RouterLink :to="{ name: 'admin_home' }" class="link link-primary">Home</RouterLink>
                </p>
            </div>
        </div>
    </div>
</template>