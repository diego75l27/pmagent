import gradio as gr
from neo4j import GraphDatabase
import pandas as pd


class NodeUploader:
    def __init__(self, uri, username, password):
        self.uri = uri
        self.username = username
        self.password = password
        self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))

    def create_or_merge_task(self, session, task_id, task_name, budgeted_cost):
        session.run(
            "MERGE (t:Task {id: $task_id})"
            "SET t.label = 'Task', t.name = $task_name, t.budgeted_cost = $budgeted_cost",
            task_id=task_id, task_name=task_name, budgeted_cost=budgeted_cost
        )

    def create_or_merge_period(self, session, period_id, period_name):
        session.run(
            "MERGE (p:Period {id: $period_id})"
            "SET p.label = 'Period', p.name = $period_name",
            period_id=period_id, period_name=period_name
        )

    def insert_nodes(self, data):
        with self.driver.session() as session:
            for _, row in data.iterrows():
                if row["Label"] == "Task":
                    self.create_or_merge_task(session, row["ID"], row["Name"], row["Budgeted_Cost"])
                elif row["Label"] == "Period":
                    self.create_or_merge_period(session, row["ID"], row["Name"])


class RelationshipUploader:
    def __init__(self, uri, username, password):
        self.uri = uri
        self.username = username
        self.password = password
        self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))

    def create_relationship(self, session, start_id, end_id, relation_type, pv, ac, ev):
        query = (
            "MATCH (start), (end) "
            "WHERE start.id = $start_id AND end.id = $end_id "
            "MERGE (start)-[r:" + relation_type + "{pv: $pv, ac: $ac, ev: $ev}]->(end)"
        )
        session.run(query, start_id=start_id, end_id=end_id, pv=pv, ac=ac, ev=ev)

    def insert_relationships(self, relation_data):
        with self.driver.session() as session:
            for _, row in relation_data.iterrows():
                if row["AC"] is not None:
                    row["AC"] = 0
                if row["EV"] is not None:
                    row["EV"] = 0
                self.create_relationship(
                    session, row["Start"], row["End"], row["Type"], row["PV"], row["AC"], row["EV"]
                )


# Gradio interface
class Neo4jCSVUploader:
    def __init__(self, uri, username, password):
        self.node_uploader = NodeUploader(uri, username, password)
        self.relation_uploader = RelationshipUploader(uri, username, password)

    def process_upload(self, file):
        df = pd.read_csv(file.name)
        if {'Type'}.issubset(df.columns):
            relation_data = df
            self.relation_uploader.insert_relationships(relation_data)
        else:
            node_data = df
            self.node_uploader.insert_nodes(node_data)

        return "Uploaded and inserted data into Neo4j!"

