<script setup>
import { ref } from 'vue';
import { getAPI } from '@/httpreqs';
import { useRoute } from 'vue-router';
import ProfessionalRequestSearchResults from './ProfessionalRequestSearchResults.vue';

const route = useRoute();
const professionalID = route.params.id;

const searchParameter = ref("no_results");
const searchQuery = ref("");
const results = ref([]);
const resultsType = ref("");

const message = ref("");

function searchData() {
    return {
        "pid": professionalID,
        "parameter": searchParameter.value,
        "query": searchQuery.value,
    }
}

async function onSearchClick() {
    try {
        if (searchParameter.value === "no_results") {
            message.value = "Choose Parameter from Dropdown";
            results.value = [];
        } else {
            const response = await getAPI({ url: "/api/search", params: searchData() });
            if (response.data.found) {
                resultsType.value = response.data.type;
                results.value = response.data.results;
            } else {
                results.value = [];
            }
        }
    } catch {
        message.value = "Something Went Wrong";
    }
    setTimeout(function () {
        message.value = "";
    }, 2000)
}

// SEARCH PARAMETERS WITH VALUES
const searchParams = [
    {
        id: 14,
        value: "request_service_name",
        name: "Service Request: Service Name",
    },
    {
        id: 15,
        value: "request_customer_name",
        name: "Service Request: Customer Name",
    },
    {
        id: 16,
        value: "request_professional_name",
        name: "Service Request: Professional Name",
    },
]

</script>
<template>
    <div class="card border-2 rounded-sm border-primary-content/25">
        <div class="card-body">
            <h2 class="text-lg font-semibold">SEARCH BY:</h2>
            <div v-if="message" class="bg-warning font-semibold p-4 my-4 rounded-md border-2 border-warning-content/50">
                <p class="text-center text-lg font-bold">{{ message }}</p>
            </div>
            <form class="form-control">
                <select v-model="searchParameter" class="w-96 select select-lg select-bordered border-2">
                    <option value="no_results" selected>-- SELECT ONE --</option>
                    <option v-for="param in searchParams" :key="param.id" :value="param.value">{{ param.name }}</option>
                </select>
                <input type="text" v-model="searchQuery" placeholder="Type Here" class="w-96 input input-lg input-bordered border-2 mt-4">
                <button type="button" @click.prevent="onSearchClick" class="btn btn-lg btn-primary mt-4">SEARCH</button>
            </form>
        </div>
    </div>

    <h2 class="text-lg font-semibold">RESULTS: {{ results.length }} Returned</h2>
    <div v-if="resultsType === 'SERVICE_REQUEST'" class="w-full flex justify-center items-center">
        <ProfessionalRequestSearchResults :items="results" />
    </div>
    <div v-else>
        {{ results }}
    </div>
</template>