from nonebot import on_command, CommandSession, get_bot
from nullbot.utils.helpers import multiline_msg_generator
from nullbot.utils.deco import group_only, superuser_only, admin_only, owner_only


@on_command('ls', only_to_me=False, shell_like=True)
@group_only
@admin_only
async def handle_ls(session: CommandSession):
    group_id = session.ctx['group_id']
    user_id = session.ctx['user_id']

    # args
    argv = session.args['argv']
    ls_all = True if '-a' in argv or '--all' in argv else False

    try:
        members = await session.bot.get_group_member_list(group_id=group_id)
    except Exception as e:
        print(type(e), e)
    
    lines = ['{} [{}]'.format(member['card'] if member['card'] else member['nickname'], member['user_id']) for member in members]
    
    count = len(lines)
    header = '正在获取群成员列表...共{}人'.format(count)
    try:
        await session.bot.send_msg(group_id=group_id, message=header)

        for msg in multiline_msg_generator(lines=lines, lineno=True):
            await session.bot.send_msg_rate_limited(group_id=group_id, message=msg)

            if not ls_all:
                await session.bot.send_msg(group_id=group_id, message="Try `ls -a` or `ls --all` for full message.")
                break
    except Exception as e:
        print(type(e), e)