from ochra_common.agents.task import Task
from ochra_common.agents.agent import Agent
from ochra_common.agents.scientist import Scientist
from ochra_common.agents.robot import Robot
from ochra_common.agents.manipulator import Manipulator
from ochra_common.agents.mobile_platform import MobilePlatform
from ochra_common.agents.mobile_manipulator import MobileManipulator
from ochra_common.agents.robot_task import RobotTask
from ochra_common.agents.scientist_task import ScientistTask
import uuid
from datetime import datetime, timedelta


def test_task():
    assignee_id = uuid.uuid4()
    task = Task(assignee_id=assignee_id, name="test_name")
    assert task.id != None
    assert task.cls == "ochra_common.agents.task.Task"
    assert task.assignee_id == assignee_id
    assert task.name == "test_name"
    assert task.args == {}
    assert task.status == -1
    assert task.start_timestamp == None
    assert task.end_timestamp == None

    start_timestamp = datetime.now()
    end_timestamp = datetime.now() + timedelta(minutes=1)
    task.start_timestamp = start_timestamp
    task.end_timestamp = end_timestamp

    # test task methods
    assert task.to_dict() == {
        "id": task.id,
        "cls": "ochra_common.agents.task.Task",
        "assignee_id": assignee_id,
        "name": "test_name",
        "args": {},
        "status": -1,
        "start_timestamp": start_timestamp,
        "end_timestamp": end_timestamp
    }

    assert task.to_json() == '{"id":"' + str(task.id) + '","cls":"ochra_common.agents.task.Task"' +\
        ',"assignee_id":"' + str(assignee_id) + '","name":"test_name","args":{},"status":-1,' + \
        '"start_timestamp":"' + start_timestamp.isoformat() + '","end_timestamp":"' + \
        end_timestamp.isoformat() + '"}'


def test_robot_task():
    assignee_id = uuid.uuid4()
    task = RobotTask(assignee_id=assignee_id, name="test_name")
    assert task.id != None
    assert task.cls == "ochra_common.agents.robot_task.RobotTask"
    assert task.assignee_id == assignee_id
    assert task.name == "test_name"
    assert task.args == {}
    assert task.status == -1
    assert task.start_timestamp == None
    assert task.end_timestamp == None
    assert task.priority == -1

    start_timestamp = datetime.now()
    end_timestamp = datetime.now() + timedelta(minutes=1)
    task.start_timestamp = start_timestamp
    task.end_timestamp = end_timestamp

    # test task methods
    assert task.to_dict() == {
        "id": task.id,
        "cls": "ochra_common.agents.robot_task.RobotTask",
        "assignee_id": assignee_id,
        "name": "test_name",
        "args": {},
        "status": -1,
        "start_timestamp": start_timestamp,
        "end_timestamp": end_timestamp,
        "priority": -1
    }

    assert task.to_json() == '{"id":"' + str(task.id) + '","cls":"ochra_common.agents.robot_task.RobotTask"' +\
        ',"assignee_id":"' + str(assignee_id) + '","name":"test_name","args":{},"status":-1,' + \
        '"start_timestamp":"' + start_timestamp.isoformat() + '","end_timestamp":"' + \
        end_timestamp.isoformat() + '","priority":-1}'


def test_scientist_task():
    assignee_id = uuid.uuid4()
    task = ScientistTask(assignee_id=assignee_id, name="test_name")
    assert task.id != None
    assert task.cls == "ochra_common.agents.scientist_task.ScientistTask"
    assert task.assignee_id == assignee_id
    assert task.name == "test_name"
    assert task.args == {}
    assert task.status == -1
    assert task.start_timestamp == None
    assert task.end_timestamp == None

    start_timestamp = datetime.now()
    end_timestamp = datetime.now() + timedelta(minutes=1)
    task.start_timestamp = start_timestamp
    task.end_timestamp = end_timestamp

    # test task methods
    assert task.to_dict() == {
        "id": task.id,
        "cls": "ochra_common.agents.scientist_task.ScientistTask",
        "assignee_id": assignee_id,
        "name": "test_name",
        "args": {},
        "status": -1,
        "start_timestamp": start_timestamp,
        "end_timestamp": end_timestamp
    }

    assert task.to_json() == '{"id":"' + str(task.id) + '","cls":"ochra_common.agents.scientist_task.ScientistTask"' +\
        ',"assignee_id":"' + str(assignee_id) + '","name":"test_name","args":{},"status":-1,' + \
        '"start_timestamp":"' + start_timestamp.isoformat() + '","end_timestamp":"' + \
        end_timestamp.isoformat() + '"}'


def test_agent():
    agent = Agent(name="test_name")
    assert agent.id != None
    assert agent.cls == "ochra_common.agents.agent.Agent"
    assert agent.name == "test_name"
    assert agent.status == -1
    assert agent.assigned_task == None
    assert agent.tasks_history == []

    # test agent methods
    assert agent.to_dict() == {
        "id": agent.id,
        "cls": "ochra_common.agents.agent.Agent",
        "name": "test_name",
        "status": -1,
        "assigned_task": None,
        "tasks_history": []
    }

    assert agent.to_json() == '{"id":"' + str(agent.id) + '","cls":"ochra_common.agents.agent.Agent",' + \
        '"name":"test_name","status":-1,"assigned_task":null' + \
        ',"tasks_history":[]}'


def test_scientist():
    scientist = Scientist(name="test_scientist")
    assert scientist.id != None
    assert scientist.cls == "ochra_common.agents.scientist.Scientist"
    assert scientist.name == "test_scientist"
    assert scientist.privilege == -1
    assert scientist.assigned_task == None
    assert scientist.tasks_history == []

    # test scientist methods
    assert scientist.to_dict() == {
        "id": scientist.id,
        "cls": "ochra_common.agents.scientist.Scientist",
        "name": "test_scientist",
        "privilege": -1,
        "status": -1,
        "assigned_task": None,
        "tasks_history": []
    }

    assert scientist.to_json() == '{"id":"' + str(scientist.id) + '","cls":"ochra_common.agents.scientist.Scientist",' + \
        '"name":"test_scientist","status":-1,"assigned_task":null,"tasks_history":[],"privilege":-1}'


def test_robot():
    robot = Robot(name="test_robot", type="test_type")
    assert robot.id != None
    assert robot.cls == "ochra_common.agents.robot.Robot"
    assert robot.name == "test_robot"
    assert robot.type == "test_type"
    assert robot.location == None
    assert robot.status == -1
    assert robot.assigned_task == None
    assert robot.tasks_history == []

    # test robot methods
    assert robot.to_dict() == {
        "id": robot.id,
        "cls": "ochra_common.agents.robot.Robot",
        "type": "test_type",
        "location": None,
        "name": "test_robot",
        "status": -1,
        "assigned_task": None,
        "tasks_history": []
    }

    assert robot.to_json() == '{"id":"' + str(robot.id) + '","cls":"ochra_common.agents.robot.Robot",' + \
        '"name":"test_robot","status":-1,"assigned_task":null,"tasks_history":[],' + \
        '"type":"test_type","location":null}'


def test_manipulator():
    robot = Manipulator(name="test_robot", type="test_type",
                        available_tasks=["task1", "task2"])
    assert robot.id != None
    assert robot.cls == "ochra_common.agents.manipulator.Manipulator"
    assert robot.name == "test_robot"
    assert robot.type == "test_type"
    assert robot.location == None
    assert robot.status == -1
    assert robot.assigned_task == None
    assert robot.tasks_history == []
    assert robot.available_tasks == ["task1", "task2"]

    # test robot methods
    assert robot.to_dict() == {
        "id": robot.id,
        "cls": "ochra_common.agents.manipulator.Manipulator",
        "type": "test_type",
        "location": None,
        "name": "test_robot",
        "status": -1,
        "assigned_task": None,
        "tasks_history": [],
        "available_tasks": ["task1", "task2"]
    }

    assert robot.to_json() == '{"id":"' + str(robot.id) + '","cls":"ochra_common.agents.manipulator.Manipulator",' + \
        '"name":"test_robot","status":-1,"assigned_task":null,"tasks_history":[],' + \
        '"type":"test_type","location":null,"available_tasks":["task1","task2"]}'


def test_mobile_platform():
    robot = MobilePlatform(name="test_robot", type="test_type")
    assert robot.id != None
    assert robot.cls == "ochra_common.agents.mobile_platform.MobilePlatform"
    assert robot.name == "test_robot"
    assert robot.type == "test_type"
    assert robot.location == None
    assert robot.status == -1
    assert robot.assigned_task == None
    assert robot.tasks_history == []
    assert robot.conditions == {}

    # test robot methods
    assert robot.to_dict() == {
        "id": robot.id,
        "cls": "ochra_common.agents.mobile_platform.MobilePlatform",
        "type": "test_type",
        "location": None,
        "name": "test_robot",
        "status": -1,
        "assigned_task": None,
        "tasks_history": [],
        "conditions": {}
    }

    assert robot.to_json() == '{"id":"' + str(robot.id) + '","cls":"ochra_common.agents.mobile_platform.MobilePlatform",' + \
        '"name":"test_robot","status":-1,"assigned_task":null,"tasks_history":[],' + \
        '"type":"test_type","location":null,"conditions":{}}'


def test_mobile_manipulator():
    robot = MobileManipulator(
        name="test_robot", type="test_type", available_tasks=["task1", "task2"])
    assert robot.id != None
    assert robot.cls == "ochra_common.agents.mobile_manipulator.MobileManipulator"
    assert robot.name == "test_robot"
    assert robot.type == "test_type"
    assert robot.location == None
    assert robot.status == -1
    assert robot.assigned_task == None
    assert robot.tasks_history == []
    assert robot.available_tasks == ["task1", "task2"]
    assert robot.conditions == {}

    # test robot methods
    assert robot.to_dict() == {
        "id": robot.id,
        "cls": "ochra_common.agents.mobile_manipulator.MobileManipulator",
        "type": "test_type",
        "location": None,
        "name": "test_robot",
        "status": -1,
        "assigned_task": None,
        "tasks_history": [],
        "available_tasks": ["task1", "task2"],
        "conditions": {}
    }

    assert robot.to_json() == '{"id":"' + str(robot.id) + '","cls":"ochra_common.agents.mobile_manipulator.MobileManipulator",' + \
        '"name":"test_robot","status":-1,"assigned_task":null,"tasks_history":[],' + \
        '"type":"test_type","location":null,"conditions":{},"available_tasks":["task1","task2"]}'
