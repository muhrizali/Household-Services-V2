<script setup>
import { ref } from 'vue';
import { postAPI } from '@/httpreqs';

const name = ref('');
const description = ref('');
const price = ref('');
const timereq = ref('');

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

function addMessage(msg) {
    messages.value.push(msg);
}

async function onCreateServiceClick() {
    const response = await postAPI({ url: "/api/service", data: newServiceData() });
    if (response.data.added) {
        addMessage('Service Successfully Created');
    } else {
        addMessage('Service Could Not be Added');
    }
    setTimeout(() => {
        messages.value = [];
    }, 2000);
}

</script>
<template>
    <div class="flex items-center justify-center w-full h-fit m-8">
        <div class="card card-bordered border-2 border-primary-content/25 w-2/3">
            <div class="card-body">
                
                <form @submit.prevent="onCreateServiceClick" class="form-control">
                    
                    <h2 class="card-title text-lg">
                        ADD NEW SERVICE
                    </h2>
                    <div v-if="messages.length" class="bg-warning font-semibold p-4 my-4 rounded-md border-2 border-warning-content/50">
                        <ul>
                            <li v-for="msg in messages">{{ msg }}</li>
                        </ul>
                    </div>
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
                                    <input 
                                    v-model="description" 
                                    id="description" 
                                    type="text"
                                    required    
                                    class="textarea w-full textarea-bordered border-2"
                                    placeholder="Your Service Description" 
                                    rows="4" />
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
                                    placeholder="100, 300, 500"
                                    class="input w-full input-bordered border-2" /> 
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <label for="timreq">TIME REQUIRED:</label>
                                </td>
                                <td>
                                    <input 
                                    v-model="timereq" 
                                    id="timereq" 
                                    type="number"
                                    required
                                    min="1" 
                                    placeholder="Estimated Hours"
                                    class="input w-full input-bordered border-2" />
                                </td>
                            </tr>
                        </tbody>
                    </table>

                    <!-- Buttons Adding Services -->
                    <div class="flex items-center justify-center mt-4">
                        <input type="submit" value="CREATE SERVICE" class="btn btn-block btn-lg btn-primary" />
                    </div>
                </form>
                <p class="text-center pt-2">
                    Go back to <RouterLink :to="{ name: 'admin_home' }" class="link link-primary">Home</RouterLink>
                </p>
            </div>
        </div>
    </div>
</template>