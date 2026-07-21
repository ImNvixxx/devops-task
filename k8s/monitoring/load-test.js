import http from "k6/http";
import { sleep } from "k6";

export const options = {
    stages: [
        { duration: "30s", target: 20 },
        { duration: "1m", target: 100 },
        { duration: "30s", target: 0 },
    ],
};

export default function () {
    http.get("http://localhost:8000/");
    sleep(0.2);
}
