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

function serviceEditData() {
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
        const response = await putAPI({ url: "/api/service", data: serviceEditData() });
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
                    <form @submit.prevent="onEditClick" class="form-control">
                        <table class="table table-sm">
                            <tbody>
                                <tr>
                                    <td>
                                        <label for="name">NAME:</label>
                                    </td>
                                    <td>
                                        <input 
                                        v-model="name"
                                        id="name" 
                                        type="text"
                                        required 
                                        class="input w-full input-bordered border-2"
                                        placeholder="Clearning, Cooking, Repair" /> 
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <label for="description">DESCRIPTION:</label>
                                    </td>
                                    <td>
                                        <textarea
                                        v-model="description" 
                                        name="description" 
                                        id="description"
                                        required
                                        class="textarea w-full textarea-bordered border-2"
                                        placeholder="Your Service Description"
                                        rows="4">
                                        </textarea>
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <label for="price">PRICE:</label>
                                    </td>
                                    <td>
                                        <input 
                                        v-model="price"
                                        id="price" 
                                        type="number"
                                        required
                                        min="100" 
                                        class="input w-full input-bordered border-2"
                                        placeholder="100, 300, 500" />
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <label for="timereq">TIME REQUIRED (in hours):</label>
                                    </td>
                                    <td>
                                        <input 
                                        v-model="timereq"
                                        id="timereq" 
                                        type="number"
                                        required
                                        min="1" 
                                        class="input w-full input-bordered border-2"
                                        placeholder="Estimated Hours" />
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <div class="flex items-center justify-center mt-4">
                            <input type="submit" value="EDIT" class="btn btn-block btn-lg btn-warning" />
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