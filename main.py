from base.module import BaseModule, message, command

from pyrogram.types import Message

from base.states import StateMachine, State


class ExampleMachine(StateMachine):
    name_state = State()
    age_state = State()


class FSMExampleModule(BaseModule):
    @property
    def state_machine(self) -> StateMachine:
        return ExampleMachine

    @command("fsm_start")
    async def fsm_start(self, message: Message, fsm: ExampleMachine):
        await message.reply("Hello! What's your name?")
        fsm.name_state.set()
    
    @message(fsm_state=ExampleMachine.name_state)
    async def recv_name(self, message: Message, fsm: ExampleMachine):
        await message.reply(f"Hello {message.text}! What's your age?")
        fsm.update_data(name=message.text)
        fsm.age_state.set()

    @message(fsm_state=ExampleMachine.age_state)
    async def recv_age(self, message: Message, fsm: ExampleMachine):
        await message.reply(f"Nice! Your name is {fsm.get_data('name')} and you're {message.text} years old!")
        fsm.clear()
