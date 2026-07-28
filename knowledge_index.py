"""
Multithreaded Inverted Index and Knowledge Retrieval Engine

This script implements a thread-safe, high-performance inverted index designed for 
concurrent document ingestion and fast keyword-based search operations. 

Key Components:
- ThreadSafeIngestionCache: Manages thread-safe batching and deferred flushing 
  of document updates to prevent excessive lock contention during heavy parallel loads.
- KnowledgeIndex: Core inverted index that tokenizes, sanitizes, and maps 
  normalized keywords to sets of unique document IDs, enabling fast set-intersection 
  queries.
- Concurrent Worker Simulation: Utilizes a ThreadPoolExecutor to simulate asynchronous, 
  multi-worker ingestion pipelines across distributed data slices.
"""

import re
import threading
import concurrent.futures

class ThreadSafeIngestionCache:
    def __init__(self, idx: "KnowledgeIndex"):
        self.attached_index = idx
        self.to_add = []
        self.write_lock = threading.Lock()


    def add_to_cache(self, data_tuple): 
        with self.write_lock:
            self.to_add.append(data_tuple)


    def flush_to_index(self):
        with self.write_lock:
            items_to_flush = self.to_add
            self.to_add = []

        # let the other threads start adding to the in-memory list
        with self.attached_index.write_lock:
            for data in items_to_flush:
                doc_id, words = data

                for word in words:
                    if word in self.attached_index.doc_base:
                        self.attached_index.doc_base[word].add(doc_id)
                    else:
                        self.attached_index.doc_base[word] = {doc_id}


class KnowledgeIndex:
    def __init__(self):
        self.doc_base = {}
        self.cache = ThreadSafeIngestionCache(self)
        self.write_lock = threading.Lock()


    def display(self):
        print("{}".format(self.doc_base))


    def sanitize_words(self, text):
        return [re.sub(r"[?.,!]", "", word).casefold() for word in text.split()]


    def add_document(self, doc_id: int, text: str) -> None:
        clean_list = self.sanitize_words(text)
        self.cache.add_to_cache((doc_id, clean_list))


    def search(self, query: str) -> set:
        clean_list = self.sanitize_words(query)

        if not clean_list:
            return set()

        ret_set = self.doc_base.get(clean_list[0], set())

        for word in clean_list[1:]:
            word_docs = self.doc_base.get(word, set())
            ret_set = ret_set & word_docs

            if not ret_set:
                break
            
        return ret_set


def doc_search(shared_index, string):
    if string not in shared_index.doc_base:
        print("{} = None".format(string))
    else:
        print("{} = {}".format(string, shared_index.doc_base[string]))


def worker_add_docs(shared_index, worker_offset, num_workers):
    data_tuples = [
        ("Cloud deployment scaling metrics", 4821),
        ("Distributed consensus algorithms in practice", 9123),
        ("High throughput log aggregation pipelines", 3412),
        ("Container orchestration failure recovery", 7854),
        ("Latency reduction in microservice architectures", 1209),
        ("Automated database failover mechanisms", 6543),
        ("Zero downtime rolling update strategies", 8932),
        ("Infrastructure as code syntax validation", 2314),
        ("Network packet inspection and routing", 5678),
        ("Secure token authentication protocols", 4312),
        ("Memory leak detection in backend workers", 9871),
        ("Thread pool starvation debugging tips", 3456),
        ("Load balancer health check configurations", 6789),
        ("Cryptographic key rotation workflows", 1123),
        ("Garbage collection tuning for low latency", 4589),
        ("Event driven architecture message queues", 7234),
        ("CI pipeline optimization and caching", 3891),
        ("Edge computing caching layer design", 6123),
        ("Storage volume snapshot replication", 9452),
        ("API gateway rate limiting strategies", 2839),
        ("Real time telemetry data collection", 5192),
        ("Serverless function cold start mitigation", 7812),
        ("Virtual private cloud peering setup", 3491),
        ("Secure shell tunneling configurations", 6241),
        ("Automated security vulnerability scanning", 8934),
        ("Horizontal pod autoscaling triggers", 1423),
        ("Distributed tracing context propagation", 5892),
        ("Database indexing optimization patterns", 7341),
        ("Microservices service mesh integration", 2918),
        ("Stateful application migration protocols", 6721),
        ("Continuous deployment gate validation", 4892),
        ("Log rotation and retention policies", 9134),
        ("Ephemeral environment provisioning scripts", 3215),
        ("DNS propagation delay troubleshooting", 7652),
        ("Cache invalidation race condition fixes", 5421),
        ("Webhook payload signature verification", 8391),
        ("Asynchronous task queue monitoring", 1928),
        ("Kubernetes cluster node draining", 6423),
        ("Infrastructure cost attribution tagging", 3194),
        ("Network bandwidth throttling analysis", 7823),
        ("Binary serialization format benchmarks", 4912),
        ("Immutable infrastructure deployment patterns", 6234),
        ("Service level objective tracking metrics", 8123),
        ("Backup verification and restoration tests", 2451),
        ("Multi region disaster recovery design", 5789),
        ("Code review automation workflow bots", 9314),
        ("Container vulnerability patching cycles", 3821),
        ("Configuration drift detection alarms", 6492),
        ("API versioning deprecation timelines", 1234),
        ("SSL certificate expiration monitoring", 7589),
        ("Database connection pool saturation", 4123),
        ("Message broker partition rebalancing", 8941),
        ("High availability cluster heartbeats", 3512),
        ("Root cause analysis documentation templates", 6891),
        ("Synthetic user transaction monitoring", 2345),
        ("Static code analysis rule customization", 7123),
        ("In-memory data store persistence modes", 5489),
        ("Distributed lock manager implementation", 9234),
        ("Continuous integration build matrix setup", 3781),
        ("Network partition simulation testing", 6342),
        ("Garbage collection pause time analysis", 8192),
        ("Secret management vault access policies", 2941),
        ("Blue green deployment routing switches", 5612),
        ("Packet loss diagnosis in transit", 7483),
        ("Database query execution plan tuning", 1829),
        ("Microfrontend architecture state sharing", 6923),
        ("Container image layer optimization", 4351),
        ("Automated backup encryption standards", 8712),
        ("Queue depth alerting threshold rules", 3245),
        ("Zero trust network access boundaries", 6124),
        ("Fault tolerant state machine design", 9812),
        ("CPU throttling metrics in cloud VMs", 4591),
        ("Load testing script concurrency spikes", 7312),
        ("Application performance monitoring agents", 2894),
        ("DNS resolution failure mitigation", 6412),
        ("Server hardware health telemetry", 8923),
        ("Distributed system transaction rollback", 3124),
        ("Continuous delivery pipeline bottlenecks", 5712),
        ("Memory allocation profiling techniques", 7943),
        ("Automated infrastructure provisioning runs", 2481),
        ("Service mesh mutual TLS setup", 6312),
        ("Rate limiting token bucket algorithms", 4923),
        ("Log aggregation parsing regex patterns", 8512),
        ("Immutable ledger transaction integrity", 3719),
        ("Database migration rollback strategies", 7241),
        ("Ephemeral storage volume management", 1982),
        ("Network latency spike investigation", 6523),
        ("Automated dependency update checkers", 4891),
        ("Microservice API contract testing", 9324),
        ("Distributed file system consistency", 3128),
        ("Cache hit ratio optimization tuning", 7612),
        ("Container runtime security sandboxing", 5423),
        ("Infrastructure drift remediation scripts", 8194),
        ("Asynchronous event processing loops", 2351),
        ("Load balancer session persistence rules", 6781),
        ("Database index fragmentation analysis", 4192),
        ("Real time metrics aggregation pipelines", 8921),
        ("Serverless function timeout handling", 3421),
        ("Multi-tenancy isolation boundary checks", 7192),
        ("Distributed tracing latency breakdown", 5834)
    ]
    
    offsets = [x for x in range(worker_offset - 1, len(data_tuples), num_workers)]

    for idx in offsets:
        text, doc_id = data_tuples[idx]
        shared_index.add_document(doc_id, text)


if __name__ == "__main__":
    shared_index = KnowledgeIndex()
    max_workers = 4

    # Use a ThreadPoolExecutor to simulate concurrent ingestion 
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # Submit multiple ingestion threads with different starting doc IDs
        futures = [
            executor.submit(worker_add_docs, shared_index, 1, max_workers),
            executor.submit(worker_add_docs, shared_index, 2, max_workers),
            executor.submit(worker_add_docs, shared_index, 3, max_workers),
            executor.submit(worker_add_docs, shared_index, 4, max_workers)
        ]

        concurrent.futures.wait(futures)

    print("Flushing cache to index...")
    shared_index.cache.flush_to_index()

    doc_search(shared_index, "distributed")
    doc_search(shared_index, "analysis")
    doc_search(shared_index, "management")
    doc_search(shared_index, "metrics")
    doc_search(shared_index, "zero_count")
