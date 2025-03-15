<script setup>
import { getAPI, putAPI } from '@/httpreqs';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const professionalID = route.params.id;

const professionalFound = ref(false);
const professional = ref({});

const message = ref('');

const fullname = ref('');
const username = ref('');
const email = ref('');

const experience = ref('');
const description = ref('');

const address = ref('');
const contact = ref('')
const pincode = ref('');

function professionalEditData() {
    return {
        'id': professionalID,
        'fullname': fullname.value,
        'username': username.value,
        'email': email.value,
        'experience': experience.value,
        'description': description.value,
        'address': address.value,
        'contact': contact.value,
        'pincode': pincode.value,
        'edit_profile': true,
    }
}

async function initialLoad() {
    const response = await getAPI({ url: '/api/professional', params: { id: professionalID } });
    if (response.data.found) {
        professionalFound.value = true;
        professional.value = response.data.professional;
        
        fullname.value = professional.value.user.fullname;
        username.value = professional.value.user.username;
        email.value = professional.value.user.email;
        experience.value = professional.value.experience;
        description.value = professional.value.description;
        address.value = professional.value.address;
        contact.value = professional.value.contact; 
        pincode.value = professional.value.pincode;
    } else {
        message.value = 'Professional Not Found';
    }
}

async function onSubmitClick () {
    const response = await putAPI({ url: '/api/professional', data: professionalEditData() });
    if (response.data.edited) {
        message.value = 'Professional Profile Edited Successfully';
    } else {
        message.value = 'Could not edit professional profile';
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
            
            <div v-if="professionalFound">
                <form class="form-control">
                    <table class="table table-lg">
                        <tbody>

                            <tr>
                                <td>
                                    <label for="fullname">FULL NAME:</label>
                                </td>
                                <td>
                                    <input v-model="fullname" type="text" id="fullname" class="input w-full input-bordered">
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <label for="username">USERNAME:</label>
                                </td>
                                <td>
                                    <input v-model="username" type="text" id="username" class="input w-full input-bordered">
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <label for="email">EMAIL:</label>
                                </td>
                                <td>
                                    <input v-model="email" id="email" type="email" class="input w-full input-bordered">
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <label for="experience">EXPERIENCE:</label>
                                </td>
                                <td>
                                    <input v-model="experience" id="experience" type="number" class="input w-full input-bordered">
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <label for="description">DESCRIPTION:</label>
                                </td>
                                <td>
                                    <input v-model="description" id="description" type="text" class="input w-full input-bordered">
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <label for="contact">CONTACT:</label>
                                </td>
                                <td>
                                    <input v-model="contact" id="contact" type="text" class="input w-full input-bordered">
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
                                    <input v-model="pincode" id="pincode" type="text" class="input w-full input-bordered">
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <button @click.prevent="onSubmitClick" class="btn btn-block btn-lg btn-warning mt-8">EDIT</button>
                </form>
            </div>
            <div v-else>
                <p class="text-center text-lg font-bold">Requested customer not found</p>
            </div>
            <p class="text-center pt-2">
                Go back to <RouterLink :to="{ name: 'professional_home' }" class="link link-primary">Home</RouterLink>
            </p>
        </div>

    </div>
</template>