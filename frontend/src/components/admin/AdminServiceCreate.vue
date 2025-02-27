<script setup>
import { ref } from 'vue';
import { postAPI } from '@/httpreqs';

const name = ref("");
const description = ref("");
const price = ref(0);
const timereq = ref(0);

const haveMessages = ref(false);
const messages = ref([]);

let newServiceData = () => {
    return {
        "name": name.value,
        "description": description.value,
        "price": price.value,
        "timereq": timereq.value
    };
};

function addFlashMessage(msg) {
    messages.value.push(msg);
}

async function onCreateServiceClick() {
    try {
        const response = await postAPI({ url: "/api/service", data: newServiceData() });
        haveMessages.value = true;
        addFlashMessage(response.data.message);
    } catch (error) {
        addFlashMessage("Some Error Occurred");
    }
}

</script>
<template>
    <!-- Add new service form -->
    <div class="flex items-center justify-center w-full h-fit m-8">
        <div class="card card-bordered border-2 border-primary-content/25 w-2/3">
            <div class="card-body">
                
                <form class="form-control">
                    
                    <!-- Form Errors -->
                    <!-- {% include "form_errors.html" %} -->
                    
                    <!-- FLASK FLASH MESSAGES -->
                    <!-- {% include "flashes.html" %} -->
                    
                    <h2 class="card-title text-lg">
                        ADD NEW SERVICE
                    </h2>
                    <div v-if="haveMessages" class="bg-warning font-semibold p-4 my-4 rounded-md border-2 border-warning-content/50">
                        <ul>
                            <li v-for="msg in messages">{{ msg }}</li>
                        </ul>
                    </div>
                    <!-- {{ newServiceData() }} -->
                    <table class="table table-sm">
                        <tbody>

                            <tr>
                                <td>
                                    <!-- {{ form.name.label }} -->
                                    <label for="name">NAME:</label>
                                </td>
                                <td>
                                    <!-- {{ form.name(class= "input w-full input-bordered border-2", placeholder = "Cleaning,
                                    Cooking, Repair...") }} -->
                                    <input v-model="name" id="name" type="text"
                                        class="input w-full input-bordered border-2"
                                        placeholder="Clearning, Cooking, Repair">
                                </td>
                            </tr>

                            <tr>
                                <td>
                                    <!-- {{ form.description.label }} -->
                                    <label for="description">DESCRIPTION:</label>
                                </td>
                                <td>
                                    <!-- {{ form.description(placeholder = "Your service description", class= "textarea w-full textarea-bordered border-2", rows=4) }} -->
                                    <input v-model="description" id="description" type="text"
                                        class="textarea w-full textarea-bordered border-2"
                                        placeholder="Your Service Description" rows="4">
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <!-- {{ form.price.label }} -->
                                    <label for="price">PRICE:</label>
                                </td>
                                <td>
                                    <!-- {{ form.price(placeholder = "Your Price", class= "input w-full input-bordered border-2") }} -->
                                    <input v-model="price" id="price" type="number"
                                        class="input w-full input-bordered border-2" placeholder="Your Price">
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <!-- {{ form.timereq.label }} -->
                                    <label for="timreq">TIME REQUIRED (hours):</label>
                                </td>
                                <td>
                                    <!-- {{ form.timereq(class= "input w-full input-bordered border-2", placeholder = "1, 2,3...")}} -->
                                    <input v-model="timereq" id="timereq" type="number" placeholder="2, 3, 4"
                                        class="input w-full input-bordered border-2">
                                </td>
                            </tr>
                        </tbody>
                    </table>

                    <!-- Buttons Adding Services -->
                    <div class="flex items-center justify-center mt-4">
                        <button @click.prevent="onCreateServiceClick" type="submit" class="btn btn-block btn-lg btn-primary">CREATE SERVICE</button>
                    </div>
                </form>
                <p class="text-center pt-2">
                    Go back to <RouterLink :to="{ name: 'admin_home' }" class="link link-primary">Home</RouterLink>
                </p>
            </div>
        </div>
    </div>
</template>