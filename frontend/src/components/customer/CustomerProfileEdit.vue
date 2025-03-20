<script setup>
import { getAPI, putAPI } from '@/httpreqs';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const customerID = route.params.id;

const customerFound = ref(false);
const customer = ref({});

const message = ref('');

const fullname = ref('');
const username = ref('');
const email = ref('');
const address = ref('');
const contact = ref('')
const pincode = ref('');

function customerEditData() {
    return {
        'id': customerID,
        'fullname': fullname.value,
        'username': username.value,
        'email': email.value,
        'address': address.value,
        'contact': contact.value,
        'pincode': pincode.value,
        'edit_profile': true,
    }
}

async function initialLoad() {
    const response = await getAPI({ url: '/api/customer', params: { id: customerID } });
    if (response.data.found) {
        customerFound.value = true;
        customer.value = response.data.customer;
        
        fullname.value = response.data.customer.user.fullname;
        username.value = response.data.customer.user.username;
        email.value = response.data.customer.user.email;
        address.value = response.data.customer.address;
        contact.value = response.data.customer.contact; 
        pincode.value = response.data.customer.pincode;
    } else {
        message.value = 'Customer Not Found';
    }
}

async function onSubmitClick () {
    const response = await putAPI({ url: '/api/customer', data: customerEditData() });
    if (response.data.edited) {
        message.value = 'Customer Profile Edited Successfully';
    } else {
        message.value = 'Could not edit customer profile';
    }
}

onMounted(initialLoad);

</script>
<template>
    <div class="card card-bordered w-1/2">
        <div class="card-body form-control">
            <h2 class="card-title text-2xl text-center">PROFILE EDIT</h2>
            <div v-if="message" class="bg-warning font-semibold p-4 my-4 rounded-md border-2 border-warning-content/50">
                <p class="text-center text-lg font-bold">{{ message }}</p>
            </div>
            
            <div v-if="customerFound">
                <form @submit.prevent="onSubmitClick" class="form-control">
                    <table class="table table-lg">
                        <tbody>

                            <tr>
                                <td>
                                    <label for="fullname">FULL NAME:</label>
                                </td>
                                <td>
                                    <input 
                                    v-model="fullname" 
                                    type="text"
                                    maxlength="200" 
                                    id="fullname" 
                                    class="input w-full input-bordered">
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <label for="username">USERNAME:</label>
                                </td>
                                <td>
                                    <input 
                                    v-model="username" 
                                    type="text"
                                    maxlength="30" 
                                    id="username" 
                                    class="input w-full input-bordered">
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <label for="email">EMAIL:</label>
                                </td>
                                <td>
                                    <input 
                                    v-model="email" 
                                    id="email" 
                                    type="email" 
                                    class="input w-full input-bordered">
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <label for="contact">CONTACT:</label>
                                </td>
                                <td>
                                    <input 
                                    v-model="contact" 
                                    id="contact" 
                                    type="text"
                                    pattern="[0-9]{10}" 
                                    class="input w-full input-bordered">
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <label for="address">ADDRESS:</label>
                                </td>
                                <td>
                                    <textarea v-model="address" rows="4" id="address"
                                    class="textarea w-full textarea-bordered"></textarea>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <label for="pincode">PIN CODE:</label>
                                </td>
                                <td>
                                    <input 
                                    v-model="pincode" 
                                    id="pincode" 
                                    type="text"
                                    pattern="[0-9]{6}" 
                                    class="input w-full input-bordered">
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <input type="submit" value="EDIT" class="btn btn-block btn-lg btn-warning mt-8" />
                </form>
            </div>
            <div v-else>
                <p class="text-center text-lg font-bold">Requested customer not found</p>
            </div>
            <p class="text-center pt-2">
                Go back to <RouterLink :to="{ name: 'customer_home' }" class="link link-primary">Home</RouterLink>
            </p>
        </div>

    </div>
</template>