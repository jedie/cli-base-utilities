from unittest import TestCase

from cli_base.systemd.template import InvalidTemplate, TemplateKeyInfo, get_template_key_info, validate_template


class TemplateTestCase(TestCase):
    def test_validate_template(self):
        content = 'One $foo and ${bar} ?!?'
        context = dict(foo='FOO', bar='BAR')
        self.assertEqual(
            get_template_key_info(content=content, context=context),
            TemplateKeyInfo(template_keys=['bar', 'foo'], not_in_context=[], not_in_template=[], invalid_keys=[]),
        )
        validate_template(content=content, context=context)

        ##########################################################################################

        context = dict(foo='FOO')
        self.assertEqual(
            get_template_key_info(content=content, context=context),
            TemplateKeyInfo(template_keys=['bar', 'foo'], not_in_context=['bar'], not_in_template=[], invalid_keys=[]),
        )
        with self.assertRaises(InvalidTemplate) as cm:
            validate_template(content=content, context=context)
        self.assertEqual(str(cm.exception), 'Template key(s) "bar" not in context')

        ##########################################################################################

        content = 'One $foo no bar!'
        context = dict(foo='FOO', bar='BAR')
        self.assertEqual(
            get_template_key_info(content=content, context=context),
            TemplateKeyInfo(template_keys=['foo'], not_in_context=[], not_in_template=['bar'], invalid_keys=[]),
        )
        with self.assertRaises(InvalidTemplate) as cm:
            validate_template(content=content, context=context)
        self.assertEqual(str(cm.exception), 'Context key(s) "bar" not in template')

        ##########################################################################################

        content = 'One $foo and ${bar} ?!?'
        context = dict(foo='FOO', baz='666')
        self.assertEqual(
            get_template_key_info(content=content, context=context),
            TemplateKeyInfo(
                template_keys=['bar', 'foo'], not_in_context=['bar'], not_in_template=['baz'], invalid_keys=[]
            ),
        )
        with self.assertRaises(InvalidTemplate) as cm:
            validate_template(content=content, context=context)
        self.assertEqual(
            str(cm.exception), 'Template key(s) "bar" not in context & Context key(s) "baz" not in template'
        )
